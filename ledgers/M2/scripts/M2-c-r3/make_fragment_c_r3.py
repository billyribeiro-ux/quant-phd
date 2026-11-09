"""Writes the round-3 fragment ledgers/M2/M2-c.json (verifier round 3, slice c). Standard library only."""
import json, subprocess

S = "scripts/M2-c-r3/"
P = lambda name: f"ledgers/M2/{S}{name}"

def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        assert fix, rid
        r["fix"] = fix
    return r

R = []
# ---- gates, re-run this round at pin 8196077d
R.append(row("M2c-gate-check-pages", "2.9-structure", "tools/check_pages.py --unit M2",
    "PASS", f"Fresh run: {P('g01_check_pages_unit.out')} = 'check_pages M2: PASS', exit=0."))
R.append(row("M2c-gate-check-dag", "2.9-DAG", "tools/check_dag.py --unit M2",
    "PASS", f"Fresh run: {P('g02_check_dag.out')} = 'check_dag M2: PASS', exit=0."))
R.append(row("M2c-gate-run-labs", "2.5-labs", "tools/run_labs.py --unit M2 --page L13..L18",
    "PASS", f"Fresh run, one call per page: {P('g04_run_labs_L13_L18.out')} shows six 'run_labs M2: PASS (1/1)' lines, exit=0."))
R.append(row("M2c-gate-check-projects", "gate", "tools/check_projects.py --unit M2",
    "PASS", f"Fresh run: {P('g03_check_projects.out')} = 'check_projects M2: PASS', exit=0 (project slice owned elsewhere; run as a gate)."))
R.append(row("M2c-gate-page-smoke", "2.9-smoke", "tools/page_smoke.py --unit M2 --pages L13 L14 L15 L16 L17 L18",
    "PASS", f"Fresh run in the foreground: {P('g05_page_smoke_L13_L18.out')} ends 'page_smoke M2: PASS', exit=0; each page PASS."))
R.append(row("M2c-gate-pytest", "gate", "pytest tests/test_labs.py -k 'M2 or L13..L18'",
    "PASS", f"Fresh run: {P('g09_pytest_labs_M2.out')} (27 tests, exit 0). test_run_labs.py and test_page_checks.py not re-run: no file under tools/ or tests/ differs between the round-2 pin and 8196077d (git diff --stat)."))
R.append(row("M2c-verify-refs", "2.1-citations", "tools/verify_refs.py --offline; tools/verify_refs.py --unit M2",
    "PASS", f"Offline: {P('g10_verify_refs_offline.out')} '560 entries, 0 problems'. Live --unit M2: {P('g11_verify_refs_live_M2.out')} '2 of 560 entries, 0 problems', exit=0. Registry titles match the page text: hubbard2015vector 'Vector Calculus, Linear Algebra, and Differential Forms: A Unified Approach'; spivak2008calculus 'Calculus'."))
R.append(row("M2c-attribution", "2.1-attribution", "L13-L18 References sections; body text",
    "PASS", "Grep (Spivak|Hubbard|spivak|hubbard|Velleman|data-cite) over L13-L18: hits only in the References sections, which state that no passage locator is confirmed and attribute nothing. No claim carries data-cite or a registry key in the body."))
R.append(row("M2c-grades", "2.3-grades", "L13-L18 claim blocks and Key results tables",
    "PASS", f"Re-graded fresh: {P('grades_scan.out')} lists 13 claim blocks (all T, each a proved result) and 39 Key-results rows. Lab-read rows are C and name the lab. The round-2 FAIL (L14 key row 4) is fixed: the row now states nine decimals, which is exact arithmetic of Proposition 3.1 at x=2 (see M2c-L14-keyresult-grade). The L14 branch row (T) depends on an unstated convention; that defect is reported under M2c-L14-branch-comparison, not as a grade mismatch."))
R.append(row("M2c-data-figures", "2.8-data", "L13-L18 (no data-files, no chart or figure markup)",
    "PASS", "grep for data-files|data-chart|<figure|class=\"chart\" over the six pages returns 0 in each. No dataset is read and no figure is drawn, so no MANIFEST or SIMULATED label is required on these pages."))
R.append(row("M2c-notation", "13-notation", "L13-L18 math; notation/notation.json",
    "PASS", f"{P('notation_scan.out')}: no use of the registry symbols T, Phi, gamma_3, gamma_4, R^*, R^{{e*}}, R_f, Q and no registry macro (\\E, \\Prob, \\Var, \\Cov, \\tr, ...) in the six pages. \\R appears with its registered meaning (real numbers); the other macros are standard TeX."))
R.append(row("M2c-banned-scan", "1.3-1.4 banned phrases", "L13-L18 HTML, six lab twins, slice cards",
    "PASS", f"{P('banned_scan_r3.out')}: zero hits for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly. Scope words (only, every, exactly, same, most, small, smooth, any) checked in context: each is either a proved or computed statement, a stated hypothesis, or 'at most'/'for small t'."))
R.append(row("M2c-process-words", "12-process-words", "L13-L18 learner text; slice cards",
    "PASS", f"{P('banned_scan_r3.out')}: process words (architect, builder, verifier, planner, ledger, fanout, round 2/3, page_smoke, run_labs, check_pages) absent from the pages, twins and slice cards."))
R.append(row("M2c-dag-forward-mentions", "2.9-DAG / 1.10", "L13-L18 concept links and names",
    "PASS", f"{P('dag_names_scan.out')}: concept links point only backward (L13 -> L01, L04, L08 and exponential-and-logarithm in concepts.html; L14 -> L04, L13; L15 -> L01; L16 -> L04, L13; L17 -> L16; L18 -> own jacobian). Later-module names appear only as prose ('linear map' in one quiz distractor, L18.html; 'Schwarz' is Cauchy-Schwarz in L15). No dfn or link to a later concept. The L15 Introduces line says 'no concept of its own'."))
R.append(row("M2c-terms-before-definition", "2.9 / 5-terms", "L14.html:73 vs :79; L18.html:340",
    "PASS", "Carried from round 2 (course/modules/M/M2/L14.html lines 73 and 79, and course/modules/M/M2/L18.html line 340, byte-identical since the previous pin; the L14 hunks of the delta are at lines 431-475 only): the forward reference to Assumption 1 at L14.html:73 is labelled and resolved by the paragraph at :79 in the same lesson, and the o(|h|) at L18.html:340 is standard prose notation. Round-3 re-read agrees."))
R.append(row("M2c-hours", "2.9-hours", "L13-L18 data-hours; course/modules/M/M2/index.html",
    "PASS", f"{P('structure_scan.out')}: data-hours=10 on each of L13-L18 (6 to 12 h rule, check_pages line 228). The plan allots 10 h per lesson (plans/M2-build-plan.md section 3). The hub split is owned by the hub slice and is not re-checked here."))
R.append(row("M2c-structure", "2.9-structure", "L13-L18 HTML",
    "PASS", f"{P('structure_scan.out')}: why-it-matters 106, 102, 89, 95, 83, 107 words (limit 120); 3 misconceptions each; 3 problems in each of the four tiers (mech-, proof-, emp-, res-) each; 12 solution blocks each; 9-10 quiz items; lab section present once. Section order checked against BUILDER_RULES 4.2 in the file positions."))
R.append(row("M2c-quiz-keys", "2.9-quiz", "L13-L18 quiz sections (li.item, data-correct, data-answer)",
    "PASS", "Each numeric key re-derived: L13 2.5, 2, 0.1; L14 7, -0.25, 2 (quiz item numbers as in the page); L15 5, 0.5, 0.3849002 (true 0.38490018, difference 1.8e-8 inside tolerance 1e-6); L16 5, 2, 0.25, 4; L17 7.2, 10, 1; L18 3, 1. Each data-correct option checked against the lesson text. L15 item 7 has two correct readings, reported separately."))

# ---- L13
R.append(row("M2c-L13-numbers", "2.2-numbers", "course/modules/M/M2/L13.html (Example 2.3, Lab 1 prose, Sections 2-5, Problems, Key results, Misconceptions 1-2)",
    "PASS", f"Recomputed from unrounded values with {P('numbers_L13.py')} (output {P('numbers_L13.out')}) and {P('numbers_L13b.py')}: forward error at 1e-2 = 0.01363683, central 4.53049e-5; Example 2.3 bounds 0.0135914/0.0137280 and 4.4854e-5/4.5760e-5; ratio intervals (9.990, 10.101) and (98.906, 101.106); printed ratios 10.03 and 100.00 inside. Misconception 2 unrounded ratio 301.001, printed-digit ratio 301.10. Misconception 1 ratio 32.62. E2 rounding/truncation 326.74, total 4.4545e-7. E3 3delta/e=2.45057e-16, cube root 6.25781e-6. R1 2sqrt(1e-3/e)=0.0383604. R3 2^-53/1e-8=1.110e-8, times e = 3.018e-8. Section 5 2sqrt(e*2^-52)=4.9136e-8. Sweep minima at 1e-8 (forward) and 1e-5 (central). Tie claim: {P('tie_check_L13.py')} gives difference 4.44e-16 < 1e-15."))
R.append(row("M2c-L13-theorems", "2.4-math", "L13.html Thm 2.1, 2.2, Prop 3.2, Cor 4.1, Problems M1-M3, P1-P3, Section 5, Assumption 1",
    "PASS", "Re-derived by hand: Thm 2.1 and 2.2 proofs (Lagrange remainders, cancellation to h^2/12 times f'''(xi+)+f'''(xi-), midpoint m, IVT); Prop 3.2 triangle bounds 2delta and delta/h; Cor 4.1 B'(h)=M/2-2delta/h^2, B''=4delta/h^3>0, B(h*)=2sqrt(M delta); central P3 B_c'=M3 h/3-delta/h^2, B_c(h*)=3delta/(2h*) (checked numerically: 5.3224e-11 both ways). Problems M1 (0.1), M2, M3 (sin(0.01)/0.01 = 0.99998333, error -1.6667e-5), P1 (h^2), P2 (h), E1 interval 9.990-10.101. Assumption 1 users: Example 2.3, M3, E1, E2, E3, R1, R3, Section 5 bullet 1, Lab 1 each say 'Under Assumption 1' or cite it; no other use."))
R.append(row("M2c-L13-lab1", "2.5-labs", "L13.html Lab 1 (lab-M2-L13-1)",
    "PASS", f"Twin run alone under python -I -W error: {P('g06_twins_isolated_L13_L18.out')} exit 0 with the printed table. Page code equals the twin and the expected block equals the output ({P('lab_embed_check_r3.out')}). Hypothesis predictions (e h/2 = 1.36e-2; h*=1.8e-8; central step 6.3e-6) match the printed minima 1e-8 and 1e-5. Interpretation values checked against the table."))
R.append(row("M2c-L13-prose", "2.9-prose", "L13.html Assumption 1 paragraph (line 98), Section 5, Misconceptions, Key results, quiz",
    "PASS", "Re-read in full. Section 5 bullets 1-4 checked (rounding 2^-53/h; M and delta needed; noise outside the model; corner |t| gives 1 and 0). Misconceptions 1-3 checked against Prop 3.2 and the table. Quiz items 1-10: keys match the text (Q2 minimum at 1e-8 checked: 6.6028e-9 is the least of the 12 printed forward errors). Key-results rows 1-8 grades T/C consistent."))
R.append(row("M2c-L13-lab-embed", "2.5-labs", "L13.html lab-M2-L13-1 vs tests/labs/M2/lab-M2-L13-1.py",
    "PASS", f"{P('lab_embed_check_r3.out')}: code_equals_twin=True, expected_equals_output=True for L13."))

# ---- L14
R.append(row("M2c-L14-numbers", "2.2-numbers", "course/modules/M/M2/L14.html (Example 4.1, Example 5.1, Lab 1 prose, E1, Key results)",
    "PASS", f"Recomputed with {P('numbers_L14.py')} (output {P('numbers_L14.out')}): e^2 = 7.389056099, 2e^2 = 14.778112198, 3e^2 = 22.167168297, sin 2 = 0.909297427, cos 2 = -0.416146837, f(2) = 15.232760911, f'(2) = 21.731770522 (closed form unrounded 21.7317705218). E1: exp(sin 1) = 2.3197768247, cos 1 = 0.5403023059; rounded-factor product 2.5067615351; unrounded 2 exp(sin 1) cos 1 = 2.506761534986894, which rounds at ten decimals to 2.5067615350 as printed. Example 5.1 values 0.841470985, 2.841470985, 2.540302306 checked."))
R.append(row("M2c-L14-theorems", "2.4-math", "L14.html Def 2.1, Prop 3.1, Prop 5.2, Problems P1-P3, R1-R3, Section 6 branch examples",
    "PASS", "Re-derived: Def 2.1 product (ad+bc), quotient ((bc-ad)/c^2), exp and sin tangents. Prop 3.1 induction: variable, constant, sum, product, quotient (needs h(a) != 0, stated), exp and sin cases; the proof uses only the hypotheses listed. Prop 5.2 path sums for v1 (v2 + cos v1) and v2 (v1). P1 (f g' + f' g), P2 (2a e^{a^2}), P3 (quotient rule), M1 (10 + 7 eps, g'(2) = 7), M2 (-1/4), R1 (6a = f''(a) for x^3), R3 (tangents 0 and 1 for max(x,0)). The branch-test wording is reported under M2c-L14-branch-comparison."))
R.append(row("M2c-L14-assumption1-order", "5-terms", "L14.html:73 vs :79",
    "PASS", "Carried from round 2 (course/modules/M/M2/L14.html lines 73 and 79 byte-identical since the previous pin): Definition 2.1 (line 73) cites Assumption 1 and the paragraph at line 79 states it in the same lesson, before Proposition 3.1 uses it. The reference is labelled, so it is not a term used without a name. Round-3 re-read agrees."))
R.append(row("M2c-L14-lab1", "2.5-labs", "L14.html Lab 1 (lab-M2-L14-1)",
    "PASS", f"Twin run alone under python -I -W error: exit 0 and output 'grid points: 251', both max-error lines True, f1(2)=15.2327609113, f1'(2)=21.7317705218 (dual and closed form), f2'(1)=2.5067615350 (dual and closed form). Lab interpretation (lines 255) matches the output and states the Assumption 1 dependence. Docstring matches the code (251 points 0.5+i/100, Dual class, no step size)."))
R.append(row("M2c-L14-keyresult-grade", "2.3-grades / 2.2(c)", "course/modules/M/M2/L14.html:434 (Key results, row 4)",
    "PASS", f"Round-2 FAIL fixed. Row now reads 'under Assumption 1, the dual evaluation of f1 at 2 has tangent 21.731770522 at nine decimals'. Recomputed: exact closed form 21.731770521811956, which rounds at nine decimals to 21.731770522 ({P('numbers_L14.out')}); the page's own Example 4.1 sum 22.167168297 - 0.435397775 = 21.731770522 agrees. Exact arithmetic of Proposition 3.1 at x=2, so T is the right grade."))
R.append(row("M2c-L14-prose", "2.9-prose", "L14.html Section 6 bullet 1 (line 288); Misconceptions (lines 300-309); Remark (line 422); Problem sets",
    "FAIL", "Section 6 bullet 1 (line 288) describes a Python branch 'x if x > 0 else -x' applied to a dual number and says it 'takes the else branch'. The lesson defines no comparison on dual numbers, and the lab class Dual has none (see M2c-L14-branch-comparison). Other prose checked and correct: Assumption 1 paragraph (line 79) and its user list; Misconceptions 1-3 (lines 300-309); Section 5 bullets; Remark (line 422) on the proofs and the missing cost bound; problem solutions M1-M3, P1-P3, E1-E3, R1, R2.",
    fix="Apply the fix in M2c-L14-branch-comparison, then this row is PASS."))
R.append(row("M2c-L14-branch-comparison", "2.2-numbers / 2.4-math / 2.9-prose (new defect)",
    "course/modules/M/M2/L14.html:288 (Section 6 bullet 1), :414 (Problem R3 solution), :435 (Key results row 5), :493-499 (quiz item 7); course/modules/M/M2/cards.json:1497 (M2-c212) and :1539 (M2-c218)",
    "FAIL", f"Definition 2.1 (lines 68-75) defines addition, product, quotient, exp and sin on dual numbers but no comparison. Lab twin tests/labs/M2/lab-M2-L14-1.py, class Dual (lines 134-180), defines no ordering: `Dual(0.0, 1.0) > 0` raises TypeError ({P('dual_ordering_check_L14.out')}). The page's claim that the program `x if x > 0 else -x` 'sees 0+1eps, takes the else branch and returns 0-1eps' therefore relies on an unstated convention that the branch test reads the value part. The same convention underlies R3, quiz item 7, key row 5 and cards M2-c212, M2-c218.",
    fix="Add one sentence to Definition 2.1 (or to Section 6): 'A branch test reads the value part a of a dual number, so the test 0 > 0 is false; the tangent does not enter the test.' Write the example's test as x.val > 0 wherever it is shown as code. No other text changes are needed."))
R.append(row("M2c-L14-lab-embed", "2.5-labs", "L14.html lab-M2-L14-1 vs tests/labs/M2/lab-M2-L14-1.py",
    "PASS", f"{P('lab_embed_check_r3.out')}: code_equals_twin=True, expected_equals_output=True for L14."))

# ---- L15
R.append(row("M2c-L15-numbers", "2.2-numbers", "L15.html Prop 3.5, E1, E3, R3, Lab 1 interpretation (line 230), Section 4 bullet 2",
    "PASS", f"{P('numbers_L15.py')} / {P('numbers_L15.out')}: exact max |cos^2 sin| = 2/(3 sqrt 3) = 0.3849001795; at every radius 1e-1..1e-6 the sampled max |g| is 0.500000 and the sampled max |f|/r is 0.3849 at angles 35, 145, 215, 325 degrees (E1 claim verified, not only the printed digits); sampled values at r=1e-3 top out at 0.3848756 < 0.3849002 (Section 4 'lower bound' claim). Along (1/n,1/n): g = 1/2, f = 1/(2n) (0.05, 0.005, 0.0005, 0.00005 printed). M1 sqrt(6) = 2.449, |(1,2,2)| = 3, sqrt 2 = 1.4142."))
R.append(row("M2c-L15-theorems", "2.4-math", "L15.html Prop 2.1, 2.2, Def 2.3, Ex 2.4, Prop 3.1, Cor 3.2, Ex 3.3, Ex 3.4, Prop 3.5, Prop 3.6, Problems M2, P1-P3, R1-R2",
    "PASS", "Re-derived: Cauchy-Schwarz via t = -x.y/|y|^2; triangle inequality from CS; Example 2.4 ball inclusion |y-a| < s + |x-a| = r; closed disc not open (point (1+r/2,0)); Prop 3.1 bound and Cor 3.2 contrapositive; Example 3.3 |f| <= |y| <= |(x,y)|; Example 3.4 values 1/2 and 0; Prop 3.5 g = sin(2 theta)/2, f = r cos^2 sin, max of (1-s^2)s at s = 1/sqrt3 is 2/(3 sqrt3); Prop 3.6 contradiction (1/2 vs 0); P1 equality case; P2 complement open; P3 delta = sqrt(eps); R1 parabola limit 1/2 and line limits 0 (y=mx gives m x/(x^2+m^2)); R2 continuity-based openness. All hold."))
R.append(row("M2c-L15-lab1", "2.5-labs", "L15.html Lab 1 (lab-M2-L15-1) and interpretation (line 230)",
    "PASS", f"Twin run alone under python -I -W error: {P('g06_twins_isolated_L13_L18.out')} exit 0. Docstring matches code (360 samples per circle, radii 10^-k for k=1..6, sequence (1/n,1/n) for n=10..10000). Interpretation values 0.500000, 0.3849, 0.38490018 and f(1/n,1/n) = 1/(2n) match the output."))
R.append(row("M2c-L15-prose", "2.9-prose", "L15.html Section 4 (bullets 1-3), Section 5 (misconceptions 1-3), Key results (rows 1-8), Remark on R3 (line 360)",
    "PASS", "Re-read in full. Section 4 bullet 2 (the grid contains pi/4 for g; the maximiser of f is not on the 1-degree grid) checked by computation. Misconceptions 1-3 checked against Examples 3.3, 3.4 and Corollary 3.2. Key-results rows grades: T rows proved in the section named; row 8 is C and names Lab 1. R3 (changed sentence at line 360) is a correct statement about continuity at the origin. Quiz item 7 is reported separately under M2c-L15-quiz-q7-two-correct."))
R.append(row("M2c-L15-quiz-q7-two-correct", "2.9-quiz (new defect)", "course/modules/M/M2/L15.html:436-441 (quiz item 7)",
    "FAIL", "Keyed option 'Each point of the set has a ball of some radius inside the set' and distractor 'Every point is the centre of a ball lying inside the set' (line 438) are equivalent when 'every point' is read as the points of U, which Definition 2.3 quantifies over. The item therefore has two correct readings. Misconception 3 and the explanation (line 410) do not separate them.",
    fix="Reword the distractor to 'Every point of R^n is the centre of a ball lying inside the set', which is false, so the keyed option is the only correct one."))
R.append(row("M2c-L15-lab-embed", "2.5-labs", "L15.html lab-M2-L15-1 vs tests/labs/M2/lab-M2-L15-1.py",
    "PASS", f"{P('lab_embed_check_r3.out')}: code_equals_twin=True, expected_equals_output=True for L15."))

# ---- L16
R.append(row("M2c-L16-numbers", "2.2-numbers", "L16.html Example 1.3, Prop 2.1 prose, Lab 1 hypothesis, E1, E3, R3, Key results",
    "PASS", f"{P('numbers_L16_L17_L18.py')} / .out: F_x(1,2) = 4 + 2e^2 = 18.778112198 and F_y(1,2) = 1 + e^2 = 8.389056099. Lab hypothesis: max of |y^3 e^{{xy}}| on the grid = e^2 = 7.389; 8e^2 = 59.11; max |F| on the grid = 4 + e^2 = 11.389 at (2,1); rounding 1.14e-10. E1: half-ulp near 11.39 = 8.88e-16, /h = 8.88e-11; truncation 1.23e-10. R3: h^2/6*20 = 3.33e-10, delta/h = 1e-10, total 4.33e-10. E3: F_xy = F_yx = 2x + e^{{xy}} + xy e^{{xy}}; at (1,2) this equals 2 + 3e^2 = 24.167168. Remark 1.2 changed sentence is correct (one-variable rules apply to phi)."))
R.append(row("M2c-L16-theorems", "2.4-math", "L16.html Remark 1.2, Prop 2.1, Prop 3.1, Problems P1-P3, R1-R2, Assumption 1 list",
    "PASS", "Re-derived: Remark 1.2 (partial exists iff phi differentiable at 0); Prop 2.1 proof via Theorem 2.2 of L13 with phi'(a1) = partial; P1 (2 a1 a2 exact, third derivative zero); P2 (quotient 0 for every t); P3 (|t|/t, sign change; k(0,t)=0); R1 (diagonal quotient (1/2)/t unbounded); R2 (4u and 2x with the held variable). Assumption 1 users Example 1.3, Lab 1, M2, E1, E3 and the Key row 4 each say so (lines 68, 72, 112, 246, 289, 303, 343)."))
R.append(row("M2c-L16-lab1", "2.5-labs", "L16.html Lab 1 (lab-M2-L16-1)",
    "PASS", f"Twin run alone under python -I -W error: {P('g06_twins_isolated_L13_L18.out')} exit 0: grid points 12, both max errors True, F_x(1,2)=18.778112, F_y(1,2)=8.389056 (both routes), axis quotients 0.0 at t = 1e-3 and 1e-6. Interpretation and hypothesis match the output and the code (H = 1e-5, grid x in {0.5,1,1.5,2}, y in {-1,0,1})."))
R.append(row("M2c-L16-prose", "2.9-prose", "L16.html Sections 3-4 (canon bullets 1-4), Misconceptions 1-3, Key results, quiz 1-10",
    "PASS", "Canon bullet 1 (f = y is 0 in (x,y) and -1 in (x,s), s = x+y) checked. Misconception 2 (f = xy: partial y = 1 at (1,1); d/dx f(x,x) = 2 at 1) checked. Quiz keys 5, 2, 0.25, 4, 'y', 'exactly 0' distractors checked. Key results rows: T rows proved in the section named; row 5 is C naming Lab 1."))
R.append(row("M2c-L16-lab-embed", "2.5-labs", "L16.html lab-M2-L16-1 vs tests/labs/M2/lab-M2-L16-1.py",
    "PASS", f"{P('lab_embed_check_r3.out')}: code_equals_twin=True, expected_equals_output=True for L16."))

# ---- L17
R.append(row("M2c-L17-numbers", "2.2-numbers", "L17.html Example 1.2, Example 2.3, Lab 1 hypothesis and interpretation, E2, E3, R1, Section 4 bullet 4",
    "PASS", f"{P('numbers_L16_L17_L18.py')} / .out: gradient (1, 1.8775825619), length 2.1272790782, angle 61.9602 degrees. R1: maximiser of u1 + 1.8775826 u2 over the max-norm ball is (1,1) with value 2.8775826; Euclidean direction (0.4701, 0.8826) rescaled to (0.5326, 1) gives 2.4101823 < 2.8776. E3: alpha = 0.0398 degrees = 6.94e-4 rad; |w|(1-cos alpha) = 5.1e-7 < 1e-4. E2: truncation <= 1.17e-12, rounding 1e-10. Lab output (62 degrees, agreement True) matches."))
R.append(row("M2c-L17-theorems", "2.4-math", "L17.html Def 1.1, Def 2.1, Thm 2.2, Example 2.3, Thm 3.1, Section 4 bullets, Problems M1-M3, P1-P3, R2, R3",
    "PASS", "Re-derived: Theorem 2.2 telescoping with the mean value theorem of L06 on each coordinate step, u_k = 0 case, q_k -> a using continuity of the partials at a only. Theorem 3.1 identity |w-(u.w)u|^2 = |w|^2 - (u.w)^2. Example 2.3 formula cos + (1+cos 0.5) sin. R2: f(tu)/t -> sin theta for cos theta != 0 (f(tu) = t cos^2 sin/(cos^2 + t^2 sin^4)); partial in x = 2xy^5/(x^2+y^4)^2 equals 1/(2y) on x = y^2. R3 first-order change -eta|grad|^2. Assumption 1 uses in Example 1.2, Example 2.3, Lab hypothesis, E2 (all three facts, lines 293) and R1 each say so."))
R.append(row("M2c-L17-lab1", "2.5-labs", "L17.html Lab 1 (lab-M2-L17-1)",
    "PASS", f"Twin run alone under python -I -W error: {P('g06_twins_isolated_L13_L18.out')} exit 0: 360 directions, error True, gradient (1.000000, 1.877583), magnitude 2.127279, angle 61.96, sampled maximum at 62 degrees, agreement True. Interpretation matches; the statement that the lab does not test other points or functions is accurate."))
R.append(row("M2c-L17-prose", "2.9-prose", "L17.html Section 4 bullets 1-4, Misconceptions 1-3, Key results, quiz 1-10",
    "PASS", "Section 4 bullet 1 (g(tu)=cos sin, exists only in four axis directions) and bullet 3 (R1 corner (1,1) at 45 degrees) checked; bullet 4 values checked against E2. Misconceptions 1-3 consistent with Example 2.3, Section 4 and Theorem 3.1. Quiz keys 7.2, 10, 1, 'corner (1,1)', 'exists only in axis directions' checked."))
R.append(row("M2c-L17-lab-embed", "2.5-labs", "L17.html lab-M2-L17-1 vs tests/labs/M2/lab-M2-L17-1.py",
    "PASS", f"{P('lab_embed_check_r3.out')}: code_equals_twin=True, expected_equals_output=True for L17."))

# ---- L18
R.append(row("M2c-L18-numbers", "2.2-numbers", "L18.html Example 4.2, Lab 1 prose, E1-E3, Key results, Section 5 R1 partial formula",
    "PASS", f"{P('numbers_L16_L17_L18.py')} / .out: remainder identity F(a+h)-F(a)-Jh = (s1^2 - s2^2, 2 s1 s2) at s = (0.3, -0.2) gives (0.05, -0.12) and length/|h|^2 = 1.0. E1: half-ulp near 4 = 4.44e-16, /h = 4.44e-11. R1 (Section 5): d/drho(rho^2 sin(1/rho)) = 2 rho sin(1/rho) - cos(1/rho), which is -1.0 at rho_k = 1/(2 pi k) on the x-axis (checked for k=7)."))
R.append(row("M2c-L18-theorems", "2.4-math", "L18.html Prop 3.2 (l.87), Prop 3.3 (l.97), Theorem 4.1 proof (l.113)",
    "FAIL", "Prop 3.2 and Prop 3.3 proofs are valid (checked line by line: component bound, triangle inequality along unit v, |Ah| <= K|h|). Theorem 4.1 proof (line 113) defines omega(rho) as 'the largest, over i, k and points x with |x - a| <= rho' of |dF_i/dx_k(x) - dF_i/dx_k(a)|. The partials are assumed continuous only at a, so the supremum over the closed ball need not be attained and 'largest' is not licensed by the hypotheses. The bound and the limit omega(rho) -> 0 need the supremum, which is finite for small rho because continuity at a bounds each partial near a.",
    fix="In line 113 replace 'be the largest, over i, k, and points x' with 'be the supremum, over i, k, and points x', and add: 'It is finite for small rho, because continuity of each partial at a bounds it on a neighbourhood of a, and omega(rho) tends to 0 as rho tends to 0.'"))
R.append(row("M2c-L18-lab1", "2.5-labs", "L18.html Lab 1 (lab-M2-L18-1)",
    "PASS", f"Twin run alone under python -I -W error: {P('g06_twins_isolated_L13_L18.out')} exit 0: 25 grid points, error True, Jacobian rows 2.000000 -4.000000 / 4.000000 2.000000, ratios 1.0000e-01 .. 1.0000e-04. Interpretation matches; it says the lab checks one direction at one point, as the code does."))
R.append(row("M2c-L18-R2-result-named", "2.4-math / 2.9-prose", "course/modules/M/M2/L18.html:340 (Problem R2 solution)",
    "FAIL", "The solution states 'The result is the chain rule for differentiable maps: if F is differentiable at a and G at F(a), then G o F is differentiable at a with array J_G(F(a)) J_F(a)', and then says 'This lesson does not state or prove the chain rule'. The second sentence contradicts the first. The proof sketch that follows is labelled as not proved and names its steps.",
    fix="Replace 'This lesson does not state or prove the chain rule' with 'This lesson does not prove the chain rule; the array above is a candidate that the page does not establish'."))
R.append(row("M2c-L18-R2-solution-numbers", "2.2-numbers", "L18.html Problem R2 solution (line 340)",
    "PASS", "The solution contains no numerical claim. Its only quantitative statement, length of J_F(a)h at most K|h| with K the sum of absolute entries, is Proposition 3.3's bound (checked, P2)."))
R.append(row("M2c-L18-prose", "2.9-prose", "L18.html Section 5 bullets 1-4, Misconceptions 1-3, Assumption 1 paragraph (line 250), Key results, quiz 1-9",
    "PASS", "Section 5 bullet 1: partial of g = y(y^2 - x^2)/(x^2+y^2)^2, equal to 1/y on the y-axis (checked by differentiation). Bullet 2: f = x^2 y/(x^2+y^4) partials 0 and directional derivative sin theta (checked). Bullet 3 (R1 is differentiable without continuous partials) checked. Bullet 4 (step analysis) consistent. Assumption 1 is used only by M2 and R1 (and the Key row for R1), each saying so. Quiz keys 3, 1 checked."))
R.append(row("M2c-L18-lab-embed", "2.5-labs", "L18.html lab-M2-L18-1 vs tests/labs/M2/lab-M2-L18-1.py",
    "PASS", f"{P('lab_embed_check_r3.out')}: code_equals_twin=True, expected_equals_output=True for L18."))

# ---- labs and twins
R.append(row("M2c-labs-lint", "2.5-labs / 13", "tests/labs/M2/lab-M2-L13-1.py .. lab-M2-L18-1.py",
    "PASS", f"{P('g07_ruff_twins.out')}: 'All checks passed!' and 6 files already formatted. {P('g08_mypy_twins.out')}: 'Success: no issues found in 6 source files' (mypy --no-incremental)."))
R.append(row("M2c-labs-data", "2.5-labs / 2.8", "the six twins; L13-L18 lab sections",
    "PASS", "No twin opens a file, and no lab section has a data-files attribute (grep 0). The twins use the standard library only, with seeded or closed-form values and no network access."))

# ---- cards
R.append(row("M2c-cards-sample-01", "2.7-cards", "cards.json M2-c181 .. M2-c190 (L13)",
    "PASS", f"Read each card against L13 text. Definitions, Theorems 2.1 and 2.2, Prop 3.2, Cor 4.1, Example 2.3 and E1-ratio card match hypotheses and values. Numbers present in L13 ({P('cards_check_r3.out')}: no 3-decimal number missing)."))
R.append(row("M2c-cards-sample-02", "2.7-cards", "cards.json M2-c191 .. M2-c200 (L13)",
    "PASS", "C cards c191-c195 and c196-c197 name the lab and carry basis; c198 and c199 are T derivations (Prop 3.2; double spacing 2^-52 near 1 gives rounding at most 2^-53); c200 (|t| at 0) matches Section 5."))
R.append(row("M2c-cards-sample-03", "2.7-cards", "cards.json M2-c201, M2-c380, M2-c381, M2-c202 .. M2-c208 (L13-L14)",
    "PASS", "c380 lists Assumption 1 users Example 2.3, M3, E1, E2, E3, R1, R3, Section 5, Lab 1 (matches L13 line 98). c381 C (2.154e-7, 1.548e-6 printed). L14 cards c202-c205 match Def 1.1, Def 2.1, Prop 3.1 hypotheses; c206-c208 values and C basis match Example 4.1 and Lab 1."))
R.append(row("M2c-cards-sample-04", "2.7-cards", "cards.json M2-c209 .. M2-c218 (L14); M2-c212 at :1497, M2-c218 at :1539",
    "FAIL", "Cards M2-c209, M2-c210, M2-c211, M2-c213, M2-c214, M2-c215, M2-c216, M2-c217 are correct against the lesson text. M2-c212 ('x if x > 0 else 0' on 0+1eps returns tangent 0) and M2-c218 (branch example for |x| gives -1 or +1) depend on the unstated branch-test convention reported under M2c-L14-branch-comparison.",
    fix="Resolve M2c-L14-branch-comparison (state the value-part convention in Definition 2.1); then both cards are correct as written. No card text change is needed beyond what that fix implies."))
R.append(row("M2c-cards-sample-05", "2.7-cards", "cards.json M2-c219 .. M2-c228 (L14-L15); M2-c225 at :1586",
    "FAIL", "Cards c219-c224 and c226-c228 are correct and their numbers and hypotheses match L14 and L15 text. M2-c225 (closed disc not open) carries the locator '(Example 2.4, Misconception 3)'. Example 2.4 (L15.html lines 92-95) is the open-ball example and does not discuss the closed disc; the argument is in the paragraph after it (L15.html line 97), and Misconception 3 (line 256) is correct.",
    fix="Change the back of M2-c225 to end '(the paragraph after Example 2.4; Misconception 3)'."))
R.append(row("M2c-cards-sample-06", "2.7-cards", "cards.json M2-c229 .. M2-c238 (L15); M2-c234 at :1651",
    "PASS", "Round-2 FAIL fixed: M2-c234 now states one result, f(1/n,1/n) = 1/(2n) for every n (Problem E3), graded T and correct (E3 derivation). The g result is in the separate card M2-c419 (L15), and the two fronts differ. c229, c230 (Prop 3.5), c231 (Prop 3.6), c232-c233 (C with basis), c235-c238 checked."))
R.append(row("M2c-cards-sample-07", "2.7-cards", "cards.json M2-c239 .. M2-c249 (L16)",
    "PASS", "Definition 1.1, Remark 1.2, Example 1.3 (18.778112198, 8.389056099), Prop 2.1 hypotheses, C cards 244-245 (basis Lab 1), misconception cards 246-249 match the text. Gap id M2-c243 is absent (no duplicate, no missing card for any item)."))
R.append(row("M2c-cards-sample-08", "2.7-cards", "cards.json M2-c251 .. M2-c260 (L17)",
    "PASS", "Definition 1.1, Example 1.2 values (length 2.1272790782, 61.9602 degrees), Definition 2.1, Theorem 2.2 hypotheses, Example 2.3, Theorem 3.1 hypotheses, Section 4 cards c257 and c258 (R1 max 2.8775826 at (1,1)) match the text."))
R.append(row("M2c-cards-sample-09", "2.7-cards", "cards.json M2-c261 .. M2-c270 (L17-L18)",
    "PASS", "C cards c259-c261 (Lab 1, 62 degrees, 1e-4 agreement, 1e-6 error) match the printed output; Definition 2.1 and 3.1 of L18, Prop 3.2 and 3.3 (hypotheses and K-bound), Theorem 4.1 hypotheses, cards c269 and c270 match the text."))
R.append(row("M2c-cards-sample-10", "2.7-cards", "cards.json M2-c271 .. M2-c279 (L18)",
    "PASS", "C cards c271-c273 match the Lab 1 print (rows 2.000000 -4.000000 / 4.000000 2.000000; ratios 1.0000e-01..1.0000e-04). c274 (D_u F(a) = Au, Section 5), c275 (g has partials, not differentiable), c276 (f = x^2y/(x^2+y^4)), c277 (R1 sufficiency, Assumption 1), c278-c279 checked."))
R.append(row("M2c-cards-sample-11", "2.7-cards", "cards.json M2-c406, M2-c413, M2-c415, M2-c419 (L14, L15)",
    "PASS", "c406 (exp and sin of dual numbers) matches Definition 2.1 and Assumption 1. c413 matches the continuity definition in Section 3. c415 (C; g = 0.500000 and f = 0.050000000 / 0.000050000 printed) matches the lab output. c419 (new this round; g(1/n,1/n) = 1/2, T) matches Example 3.4."))
R.append(row("M2c-cards-duplicates", "2.7-cards / duplicates", "cards.json (unit-wide ids and fronts; slice cards)",
    "PASS", f"{P('cards_check_r3.out')}: 394 cards, no duplicate id, no duplicate front; no near-duplicate pair within the 103 slice cards on reading all of them."))
R.append(row("M2c-cards-numbers", "2.7-cards / 2.2", "cards.json slice cards vs L13-L18 text",
    "PASS", f"{P('cards_check_r3.out')}: every number with three or more decimals on the 103 slice backs appears in its lesson text. Printed-value cards quote the printed digits in the lesson."))
R.append(row("M2c-cards-grades", "2.3-grades / 2.7", "cards.json slice cards (103: T 66, C 22, no grade 15)",
    "PASS", f"{P('cards_check_r3.out')}: every C card has a basis; the 15 cards without grade are definitions, assumptions, misconception-free statements or the Assumption-1 cards. Each T card states a proved result or a derivation on the page."))
R.append(row("M2c-cards-coverage", "2.7-cards / coverage", "cards.json slice cards vs lesson definitions, theorems, examples, labs, misconceptions",
    "PASS", "Every definition, theorem, proposition, corollary, example, lab and misconception of L13-L18 has at least one card: L13 (c181-c201, c380-c381); L14 (c202-c219, c406); L15 (c220-c238, c413, c415, c419); L16 (c239-c249); L17 (c251-c264); L18 (c265-c279). Lab cards are C with basis."))

ids_r2 = [r["id"] for r in json.load(open("/Users/billyribeiro/.fanout/frags/S-M2-c.round2.json"))["rows"]]
ids_now = [r["id"] for r in R]
missing = [i for i in ids_r2 if i not in ids_now]
print("round-2 ids:", len(ids_r2), "missing in round 3:", missing)
assert not missing, missing
assert len(set(ids_now)) == len(ids_now)

nonpass = [r for r in R if r["status"] != "PASS"]
verdict = "PASS" if not nonpass else "FAIL"
frag = {
    "unit": "M2",
    "slice": "c",
    "round": 3,
    "verifier": "Haiku 5.5 independent verifier (fanout S3 slice c, round 3)",
    "pin": "8196077d5f56c3919d33e69888176d197d378ad4",
    "base": "round 2 fragment /Users/billyribeiro/.fanout/frags/S-M2-c.round2.json at pin 9294b914a51647c66d2dee62c4a112c76ba04900 (context; PASS rows re-derived this round, carried only where the cited lines are byte-identical). Delta 9294b914..8196077d touches course/modules/M/M2/L14.html (lines 431-475), L15.html (line 360), L16.html (line 65), cards.json (M2-c234 changed, M2-c419 added); L13, L17, L18 and all six twins byte-identical.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS3-M2-c",
    "scratch": "/tmp/m2c_r3_* (reading only); every backing script and output is under ledgers/M2/scripts/M2-c-r3/",
    "verified_at": "2026-11-09T06:30:00Z",
    "verdict": verdict,
    "rows": R,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice c = L13-L18 pages, six lab twins and the cards with lesson ids L13-L18. Round 3 read every line of the six pages (L13 478 lines, L14 542, L15 486, L16 447, L17 448, L18 467) and the six twins, and all 103 slice cards.",
        "Mutants: none required. VERIFIER_RULES 2.6 mutation testing applies to project graders; lab twins are demonstrations (rulings).",
        "Not run: full repository gates (ruff/mypy over the repo, check_pages --all, build_site --check, render_curriculum), the full pytest suite and live reference checks of keys other than spivak2008calculus and hubbard2015vector (not cited in any body text). None of these covers a file in this slice. Lab page rendering was checked by page_smoke (headless Pyodide), not by a visual screenshot.",
        "Pre-existing files in ledgers/M2/scripts/M2-c-r3/ (arithmetic_checks.py, arithmetic_checks.out, build_fragment_r3.py, card_hypothesis_scan.py, card_hypothesis_scan.out) were present before this run. I did not write them, did not rely on them and did not delete them.",
        "ledgers/M2/M2-c.json held an earlier round-11 fragment at this checkout; it has been overwritten with this round-3 fragment at the path the task specifies.",
        "Non-blocking observations (not rows): L15 Lab 1 interpretation and E1 are consistent; L14 Definition 2.1 uses Assumption 1 before its paragraph (carried PASS). L19 Theorem 2.1 (mixed partials), which L16 E3 cites, exists in L19.html (line 66/72).",
    ],
    "summary": ("FAIL: %d rows (%d PASS, %d FAIL, 0 UNVERIFIABLE). Non-PASS: M2c-L14-branch-comparison (Section 6 branch example reads x > 0 on a dual number, which the lesson and the lab Dual class do not define; fix: state the value-part convention in Definition 2.1), M2c-L14-prose (same), M2c-cards-sample-04 (M2-c212, M2-c218, same cause), M2c-L15-quiz-q7-two-correct (two correct readings), M2c-cards-sample-05 (M2-c225 locator), M2c-L18-theorems (Theorem 4.1 proof: 'largest' should be 'supremum'), M2c-L18-R2-result-named (self-contradiction at L18.html:340). Round-2 FAILs M2c-grades, M2c-L14-keyresult-grade and M2c-cards-sample-06 are fixed and PASS. All gates pass." % (len(R), len(R) - len(nonpass), len(nonpass))),
}
out = "ledgers/M2/M2-c.json"
json.dump(frag, open(out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("wrote", out, "rows", len(R), "non-pass", [r["id"] for r in nonpass], "verdict", verdict)
