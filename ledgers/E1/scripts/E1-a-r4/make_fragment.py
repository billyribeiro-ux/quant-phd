import json, subprocess
ROOT = "/tmp/verifyB4-E1-a"
R = []
def row(i, check, loc, status, ev, fix=None):
    d = {"id": i, "check": check, "location": loc, "status": status, "evidence": ev}
    if status != "PASS":
        d["fix"] = fix
    R.append(d)
CARRY = "Carried from round 3 (course/modules/E/E1/index.html byte-identical in the cited lines since aa3c26c; the round-4 delta touches index.html only at lines 34 and 163-167): "
REVERIFIED = "Re-verified in round 4 (lines read this round): "

# commands
row("E1a-cmd-check-pages", "2.9-structure", "tools/check_pages.py --unit E1", "PASS",
    "Run this round at 2657ab5: 'check_pages E1: PASS', exit 0.")
row("E1a-cmd-check-dag", "DAG", "tools/check_dag.py --unit E1", "PASS",
    "Run this round: 'check_dag E1: PASS', exit 0.")
row("E1a-cmd-run-labs", "2.5-labs", "tools/run_labs.py --unit E1", "PASS",
    "Run this round: 'run_labs E1: PASS (12/12)', exit 0 (includes lab-E1-L01-1, L02-1, L03-1).")
row("E1a-cmd-page-smoke", "2.5-labs", "tools/page_smoke.py --unit E1 --pages index L01 L02 L03", "PASS",
    "Run this round: page_smoke PASS for index, L01, L02, L03; lab preload times 0.0 s; runtime boot 1.1 s.")
row("E1a-cmd-verify-refs", "2.1-citations", "tools/verify_refs.py --offline; tools/verify_refs.py --unit E1", "PASS",
    "Run this round: offline integrity '560 entries, 0 problems'; live 're-verification of E1: 1 of 560 entries, 0 problems'.")
row("E1a-twin-L01-run", "2.5-labs", "tests/labs/E1/lab-E1-L01-1.py", "PASS",
    "python -I -W error exit 0; stdout equals the embedded expected block of L01.html line 238-255 (18 lines), script ledgers/E1/scripts/E1-a-r4/embed_vs_run.py prints 'matches run: True'.")
row("E1a-twin-L02-run", "2.5-labs", "tests/labs/E1/lab-E1-L02-1.py", "PASS",
    "python -I -W error exit 0; stdout equals the embedded expected block of L02.html lines 225-243 (19 lines), 'matches run: True' (embed_vs_run.py).")
row("E1a-twin-L03-run", "2.5-labs", "tests/labs/E1/lab-E1-L03-1.py", "PASS",
    "python -I -W error exit 0; stdout equals the embedded expected block of L03.html lines 214-221 (8 lines), 'matches run: True'.")
row("E1a-twin-lint-types", "2.5-labs", "tests/labs/E1/lab-E1-L01-1.py, lab-E1-L02-1.py, lab-E1-L03-1.py", "PASS",
    "Run this round: ruff check tests/labs/E1 'All checks passed!'; ruff format --check '12 files already formatted'; mypy --no-incremental on the three twins 'Success: no issues found in 3 source files'.")

# lab hypothesis vs output
row("E1a-lab-L01-hypothesis-vs-output", "2.5-labs", "L01.html line 156 (hypothesis) against lines 238-255 (expected)", "PASS",
    "Hypothesis: 60 steps, 61 points, midpoint 30, grid maximiser point 30 in all four cases, budget exhausted, MRS equals price ratio, off-optimum equality False. Output: 'grid: 61 points' ; point 30 in all four cases; 'budget exhausted ... True' x4; MRS equal True x4; final line 'equal: False'. Matches. Interpretation (L01 line 256): 'finite check on four price and income triples' matches the code (STEPS=60, CASES has four triples).")
row("E1a-lab-L02-hypothesis-vs-output", "2.5-labs", "L02.html line 130 (hypothesis) against lines 225-243 (expected)", "PASS",
    "Hypothesis: 73 outputs j/12, j=0..72, outputs 0 to 6 (output 'grid: outputs j / 12 ... so outputs 0 to 6'); cases 1-3 outputs 4, 4, 4/3 with profits 4, 3, 16/3 (printed 'profit 4', 'profit 3', 'profit 16/3'); case 4 same output as case 1 (printed True); sqrt(12) profit 3.7128 below 4.0000 (printed). All match.")
row("E1a-lab-L03-hypothesis-vs-output", "2.5-labs", "L03.html line 115 (hypothesis) against lines 214-221 (expected)", "PASS",
    "Hypothesis: p*=110/7, Q*=480/7; grid i/7, i=0..140 with 110 positive, 1 zero at grid point 110, 30 negative (printed 110, 1, 30); Z(20)=-30 (printed); one firm 48/7 and ratio 10 (printed); firm maximiser 48/7 for F=0 and F=100 (printed True). All match.")
row("E1a-L02-lab-docstring-differ-only-in-F", "2.5-labs", "L02.html lines 131-141 (docstring) against the code lines 153-221", "PASS",
    "Docstring: 'evaluates pi exactly on the grid q=j/12 for j=0..72'; 'prints whether cases 1 and 4 share p, c and k' (code line 207-214 prints same_inputs); 'profit at sqrt(F/k) in floating point to four decimals' (lines 216-221, :.4f); 'every case has q* on the grid' true for the four cases (j=48, 48, 16, 48). Matches the code; no docstring claim is false.")
row("E1a-L03-interp-prop21-attribution", "2.9-structure", "L03.html line 222 (interpretation)", "PASS",
    "Interpretation names Remark 1.4, Proposition 1.3 (the proof) and 'Lesson 2, Proposition 1.5' (fixed cost). L02.html line 93 states Proposition 1.5 as the fixed-cost result. The attribution is correct.")

# hub
row("E1a-hub-prereq-closure", "DAG", "index.html lines 58-64", "PASS",
    CARRY + "line 60 names M2 and says M2 requires M1 and M1 requires P0.1; closure is M1, P0.1 (plus M2 concepts linked in lines 62-63). check_dag E1 PASS (this round).")
row("E1a-hub-skip-rule", "2.9-structure", "index.html lines 70 and 154; project.html line 42", "FAIL",
    "index.html line 70: 'To skip rungs 1 and 2, you must reach the bar and answer both skill checks'; index.html line 154: 'a student must reach the placement bar and answer both skill checks'; project.html line 42 (unchanged since aa3c26c, git show aa3c26c:course/modules/E/E1/project.html line 42): 'If you met the placement bar on the module page, skip rungs 1 and 2 and start at rung 3.' The second condition (both skill checks, index.html data-skill items at lines 115 and 124) is missing from the project page.",
    "project.html line 42: add 'and answered both skill checks (marked on the module page)', so the two pages state one rule. Owner: project.html (outside this slice; the hub statements are correct).")
row("E1a-hub-m2-status", "2.9-structure", "index.html lines 60 and 70", "PASS",
    CARRY + "no 'not yet released' sentence remains at lines 60 or 70; line 65 says P0.1 is not yet released, and course/modules/P is absent at this pin.")
row("E1a-hub-placement-numbers", "2.2-numbers", "index.html lines 68-70 and items at lines 72-124", "PASS",
    CARRY + "7/9 = 77.78 % displayed 77.8; 8/9 = 88.89 % displayed 88.9; 80 % of 9 = 7.2, so eight correct is the first count at or above the bar; 9 items (grep class=item); two data-skill items (lines 115, 124); seven prerequisite items.")
row("E1a-hub-hours-split", "hours", "index.html data-hours-lessons=90, data-hours-project=30 (line 29), hours-split line 39; L01-L09 data-hours", "PASS",
    "Round-4 grep: every L01-L09 page data-hours=10; 9 x 10 = 90; project 30; 90/(90+30) = 75 %, 30/120 = 25 %, matching the split markup at lines 39-41 (widths 75% and 25%). Total 120 equals plans/E1-build-plan.md line 20 (curriculum hours 120). Arithmetic only; pace not assessed (architect ruling).")
row("E1a-hub-citation-varian", "2.1-citations", "index.html lines 169-174; references/references.json key varian2014intermediate", "PASS",
    CARRY + "registry entry status 'verified' (Varian 2014, ISBN 9780393919677); verify_refs live 1 of 560 entries, 0 problems (this round). The hub states no passage locator is confirmed and attributes no statement to it.")
row("E1a-hub-lesson-claims", "2.9-structure", "index.html lines 49-54, 138, 140-148, 154-160", "PASS",
    REVERIFIED + "objectives match lesson topics (L01 utility xy and MRS tangency; L02 profit max and p=MC; L03 linear equilibrium; L04-L09 titles in cards match lesson H1s). Card text lines 140-148 match the lesson summaries (each card says 10 h, matching data-hours=10). Ladder lines 156-159 describe the reference case a=120, b=1, c=20 as stated in project.html.")
row("E1a-banned-and-scope-words", "2.9-structure", "index.html; L01.html; L02.html; L03.html", "PASS",
    REVERIFIED + "grep for builder, verifier, round, request, unit report, roughly half, about 6 %, historically, ellipsis: no hits in learner text. Scope words read in context: 'every statement in Section 1 assumes this setting' (L03 line 59, L02 line 59, L01 line 59); 'only' occurrences (L01 lines 104, 164, 380; L02 lines 98, 141, 267, 316, 350; L03 lines 127, 287, 296) are each backed by a statement on the page (for example L02 line 267 'changes only the profit level' rests on Proposition 1.5, L03 line 296 'the only zero' rests on Step 1 of Proposition 1.3); 'proves for every case in the Setting' (L01 line 256) depends on the Proposition 1.4 proof, see E1a-L01-prop-1-2-to-1-4.")
row("E1a-data-status", "2.9-structure", "index.html lines 37 and 164-167; tests/labs/E1/*.py; project.html line 316; grader/instance.py line 3", "PASS",
    REVERIFIED + "no lab reads a file (grep open( and read_text on tests/labs/E1: no hits). Exact fractions in L01 and L03 twins; L02 twin states 'floating point to four decimals' (docstring line 10) and does so for one line; L05 and L09 convert Fractions to float only for printing. The project instance is labelled SIMULATED (project.html line 316, grader/instance.py line 3).")
row("E1a-grades-and-legend", "2.3-grades", "index.html line 65; L01.html lines 42-49 and T-graded blocks; L02 and L03 equivalents", "PASS",
    REVERIFIED + "legend matches BLUEPRINT section 3 vocabulary. Graded T blocks: L01 Prop 1.2, 1.3, 1.4, 2.2, 2.3; L02 Prop 1.3, 1.5, 2.2; L03 Prop 1.3, 2.1. The grade T of L01 Prop 1.4 depends on its proof, which has a gap (row E1a-L01-prop-1-2-to-1-4).")

# L01
row("E1a-L01-prop-1-2-to-1-4", "2.4-maths", "L01.html lines 67-70 (Assumption 1), 92-105 (Proposition 1.4 and proof), 256 (interpretation), 404 (key results)", "FAIL",
    REVERIFIED + "Proposition 1.4 states that the optimal bundle over B is unique and equals (m/(2p_x), m/(2p_y)). The proof (lines 100-104) shows only that the maximiser of f on the budget line is x_0 (f(x) = m^2/(4p_xp_y) - (p_x/p_y)(x-x_0)^2), and it begins from 'an optimal bundle lies on the budget line' (Proposition 1.3), which presupposes that an optimum exists. Two steps are missing: (i) existence over all of B, and (ii) that a bundle with slack is beaten by a line bundle with utility at most f(x_0) (the Proposition 1.3 argument). Assumption 1 (line 69) says Proposition 1.4 does not use the extreme value theorem 'because its proof finds the largest value directly', which the proof does not do: it finds the largest value on the line only. The interpretation (line 256) says Proposition 1.4 proves the optimum 'for every case in the Setting', and the key-results row (line 404) grades the claim T.",
    "Insert after line 104: 'A bundle in B with slack is beaten, by the argument of Proposition 1.3, by a bundle on the line; every bundle on the line has utility at most f(x_0) = m^2/(4p_xp_y). So (x_0, m/(2p_y)) is an optimal bundle over B, and it is the only one.' Then either drop the sentence 'because its proof finds the largest value directly' from Assumption 1 and say Proposition 1.4 does not need Assumption 1 because it exhibits the optimum, or name Assumption 1 as used for existence. Confirm the same sentence in the key-results row.")
row("E1a-L01-R2-conditional-proof", "2.4-maths", "L01.html lines 378-383 (R2 solution), 496 (references)", "FAIL",
    REVERIFIED + "R2 states 'show that the optimal bundle spends the share a'. The solution takes an optimal bundle as given (Step 1 'the optimal bundle has x>0 and y>0'; Step 2 'the optimal x-bar lies in this open interval') and the references line says R2 is 'proved under Assumption 2'. Existence of a maximiser for u = x^a y^(1-a) on B is not supplied by Assumption 2 and is not stated as a hypothesis (the argument of Proposition 1.2 needs Assumption 1). Algebra in Step 3 rechecked: a y/((1-a) x) = p_x/p_y gives p_x x = a m. Only the hypothesis is missing.",
    "State the hypothesis in the problem line: 'Assuming Assumption 1 (so an optimal bundle exists) and Assumption 2'. Update line 496 to match.")
row("E1a-L01-canon-comparative-static-reason", "2.6-causal", "L01.html line 266 (Section 3, bullet 4)", "FAIL",
    "Bullet 4 reads: 'The lesson does not derive the response of the optimal bundle to a change in price as a comparative-static result, since Proposition 1.4 gives the bundle at each price separately.' The 'since' clause is a non-sequitur: Proposition 1.4's closed form x-bar = m/(2p_x) is a function of p_x, so the price response is read off it directly (d x-bar/d p_x = -m/(2p_x^2)); being given at each price does not prevent it. The bullet's claim that the lesson does not state the response as a result is true (a grep of L01 finds no derivative of x-bar with respect to p_x).",
    "Delete the 'since' clause, for example: 'The lesson does not state the response of the optimal bundle to a change in price as a comparative-static result.' Keep the Lesson 4 pointer.")
row("E1a-L01-prop-2-2-2-3", "2.4-maths", "L01.html lines 129-147", "PASS",
    REVERIFIED + "Proposition 2.2: d u/dx = y, d u/dy = x by differentiation of xy; MRS = y/x for x>0 (proof lines 135-137). Proposition 2.3: MRS = ybar/xbar = (m/(2p_y))/(m/(2p_x)) = p_x/p_y using Proposition 1.4 values (recomputed: 1/2p_y divided by 1/2p_x = p_x/p_y). Positivity of xbar, ybar is stated (line 146).")
row("E1a-L01-remark-1-5-1-7", "2.4-maths", "L01.html lines 107-120", "PASS",
    REVERIFIED + "Remark 1.5: f'(x) = (m - 2p_x x)/p_y, f''(x) = -2p_x/p_y < 0 (recomputed). Remark 1.7: the ln argument restricted to u>0; the maximum is positive so the optimum is unchanged. The phrase 'and has no other meaning' is removed from the first sentence; the claim now made is 'The number 600 ranks bundles'.")
row("E1a-L01-prop-1-2-to-1-4-proof-check", "2.4-maths", "L01.html lines 72-90 (Propositions 1.2 and 1.3)", "PASS",
    REVERIFIED + "Proposition 1.2 proof: nonempty (0,0), closed, bounded, u continuous, Assumption 1 applied; correct and conditional on Assumption 1 as stated. Proposition 1.3 proof: slack argument t = s/p_x, utility (x+t)y > xy since y>0; positivity of the candidate's utility; all recomputed.")
row("E1a-L01-remark-2-4-numbers", "2.2-numbers", "L01.html line 151", "PASS",
    REVERIFIED + "(80/3)/20 = 4/3; p_x/p_y = 2/3; one unit of x costs 2 = (2/3)*3; f'(20) = (120 - 2*2*20)/3 = 40/3 > 0; the optimum at x = 30 where MRS = 2/3 (Proposition 1.4). All recomputed by hand from the text.")
row("E1a-L01-E2-problem-exact-change", "2.2-numbers", "L01.html lines 352-356", "PASS",
    REVERIFIED + "new bundle (21, 26); utility 546; old 1600/3; change 38/3; first-order estimate 40/3 (y dx + x dy = 80/3 - 40/3); difference -2/3 equals -2 dx^2/3 at dx = 1 (expansion checked).")
row("E1a-L01-problem-set", "2.4-maths", "L01.html lines 293-364 (M1-M3, P1-P3, E1-E3)", "PASS",
    REVERIFIED + "M1: xbar = 45/4, ybar = 9, u* = 405/4, budget 90 (recomputed). M2: MRS 4/3. M3: doubling and quadrupling. P1: scaling invariance. P2: u* = m^2/(4p_xp_y) strictly increasing. P3: MRS cancellation with positivity steps named. E1: printed 625 matches case 2 output. E3: spacing 1 and grid point 30 (recomputed).")
row("E1a-L01-why-it-matters-forward-ref", "2.9-structure", "L01.html line 51", "PASS",
    CARRY + "line 51 'Section 2 names that ratio the marginal rate of substitution' matches Definition 2.1.")
row("E1a-L01-l259-false-cross-reference", "2.6-causal", "L01.html line 266 (Lesson 4 pointer)", "PASS",
    REVERIFIED + "'Lesson 4 treats how an equilibrium price moves when a demand parameter moves' matches the L04 card title and the hub's lesson map (line 143: change in an equilibrium from a demand shift). Not a false cross-reference.")
row("E1a-L01-misconceptions-and-quiz", "2.9-structure", "L01.html lines 270-286 and 412-491", "PASS",
    REVERIFIED + "misconception 1 (budget binds, (30, 20) costs 120); misconception 2 (x + y gives MRS 1); misconception 3 ((20, 80/3) MRS 4/3 vs 2/3). Quiz items 1-11 keys recomputed: 30, 20, 625, 4/3, 2/3, x for d(xy)/dy, doubles, 1 for x + y.")
row("E1a-L01-prop-1-2-to-1-4-key-results", "2.9-structure", "L01.html lines 402-406 (key results)", "FAIL",
    REVERIFIED + "The row for Proposition 1.4 grades T with 'Proved in Section 1 by completing the square', which the proof gap in E1a-L01-prop-1-2-to-1-4 does not yet support (existence and optimality over B are not shown).",
    "Resolved with E1a-L01-prop-1-2-to-1-4.")

# L02
row("E1a-L02-prop-1-3-1-5", "2.4-maths", "L02.html lines 72-99", "PASS",
    REVERIFIED + "pi(q) = pi0 - k(q - q0)^2 expansion recomputed; maximiser over q>=0 is max(0, q0) by the nearest-point argument (k>0), unique; MC(q0) = p. Proposition 1.5 proof: the output does not contain F. The maximiser exists by the completed square, so no existence gap.")
row("E1a-L02-example-1-4-and-remarks", "2.2-numbers", "L02.html lines 87-89, 101-109", "PASS",
    REVERIFIED + "C(4) = 12 + 8 + 16 = 36; profit 4; MC(4) = 10. Remark 1.6: pi(q*) - pi(0) = (p-c)^2/(4k) (recomputed); F = 100 gives -84 > -100. Remark 1.7: k = 0 cases recomputed.")
row("E1a-L02-supply-and-problems", "2.4-maths", "L02.html lines 113-126, 280-376", "PASS",
    REVERIFIED + "Definition 2.1 and Proposition 2.2 (monotone, unique MC inverse). M1: q* = 2, profit 8 (C = 4q + 2q^2, p = 12). M2: pi = -41 vs -50 (recomputed). M3: q(7) = 4, q(2) = 0. P1-P3 proofs recomputed. E1-E3 numbers: 4/3, 16/3, 3.7128, 4.0000, 88 = 100 - 12. R1: pi*'(p) = q(p), second derivative 1/(2k). R2: IFT as Assumption 1 stated, chain rule recomputed.")
row("E1a-L02-R3-threshold", "2.2-numbers", "L02.html line 377", "PASS",
    REVERIFIED + "profit (p-c)^2/(4k) - F >= 0 iff p - c >= 2 sqrt(kF) for p > c; threshold c + 2 sqrt(kF) = 2 + 2 sqrt(12) = 8.9282 (displayed 'about 8.93'); below 10 (Example 1.4 price). Recomputed.")
row("E1a-L02-misconceptions", "2.2-numbers", "L02.html lines 259-270", "PASS",
    REVERIFIED + "average cost minimum at sqrt(F/k) = sqrt(12); profit 10 sqrt(12) - (12 + 2 sqrt(12) + 12) = 16 sqrt(3) - 24 = 3.7128 (recomputed: 27.7128129 - 24); misconception 3 shutdown claim: pi(q*) + F = (p-c)^2/(4k) >= 0 for every price (recomputed).")
row("E1a-L02-quiz", "2.9-structure", "L02.html lines 398-478", "PASS",
    REVERIFIED + "Quiz items 1-11: q* = 4 (10 - 2)/2; profit 4; MC(4) = 10; supply(7) = 4; profit 3 at case 2 (28 - 25); negative-profit explanation with -84 and -F. Keys recomputed.")
row("E1a-L02-canon-wording", "2.9-structure", "L02.html lines 250-255", "PASS",
    REVERIFIED + "Bullet 4 now says the closed form of Proposition 1.3 is 'specific to the quadratic cost of the Setting', a claim of scope that Proposition 1.3 supports (the closed form uses C'(q) = c + 2kq). Bullet 2 'Remark 1.7 shows that with constant marginal cost and a price above unit cost no profit-maximizing output exists' matches Remark 1.7 (k = 0).")
row("E1a-L02-remark-1-6-domain", "2.4-maths", "L02.html line 103", "PASS",
    REVERIFIED + "pi(q*) - pi(0) = (p-c)^2/(4k) for p >= c (recomputed); domain stated as p >= c.")
row("E1a-L02-why-it-matters-pmc", "2.9-structure", "L02.html line 51", "PASS",
    REVERIFIED + "the why-it-matters paragraph: Lesson 3 uses the supply function (Lesson 3 Setting line 57 uses Proposition 2.2 of Lesson 2, checked); 'at a positive output price equals the rate at which total cost rises' matches Proposition 1.3 and Definition 1.2.")
row("E1a-L02-R2-without-closed-form", "2.4-maths", "L02.html lines 364-370", "PASS",
    REVERIFIED + "uses the first-order condition and the chain rule; IFT is stated as Assumption 1 in the solution and in the references line (487). The second derivative -2k only identifies the maximiser. d pi*/dp = q* + (p - MC(q*)) dq*/dp, the second term zero by the FOC (recomputed).")

# L03
row("E1a-L03-prop-1-3", "2.4-maths", "L03.html lines 72-84", "PASS",
    REVERIFIED + "Step 1 Z continuous and strictly decreasing (slopes -b and -(b+s)); Step 2 p* = (a+sc)/(b+s), p* - c = (a - bc)/(b+s) > 0; Step 3 uniqueness by strict monotonicity; Q* = s(p*-c) > 0. Recomputed symbolically.")
row("E1a-L03-example-1-5-and-remarks", "2.2-numbers", "L03.html lines 91-111", "PASS",
    REVERIFIED + "a=100, b=2, n=10, c=2, k=1: s=5; p* = 110/7; Q* = 480/7; D(110/7) = 480/7; S(110/7) = 5 * 96/7 = 480/7. Remark 2.2: one firm (p*-c)/(2k) = 48/7; ten firms 480/7.")
row("E1a-L03-remark-1-4-and-proof-sign", "2.4-maths", "L03.html lines 79-89", "PASS",
    REVERIFIED + "sign pattern from strict decrease of Z; 'the lesson does not analyze the speed of such a rule' is an accurate scope limit.")
row("E1a-L03-canon-and-misconceptions", "2.9-structure", "L03.html lines 225-252", "PASS",
    REVERIFIED + "Canon bullet 1: profit at p* with F = 0 is (p*-c)^2/(4k) > 0 (recomputed). Bullet 2: strict decrease of Z from strict decrease of D and monotone S. Misconceptions 1-3 values: D(20) = 60, S(20) = 90, Z = -30; one firm 48/7 vs demand 480/7; F does not change output.")
row("E1a-L03-need-not-unique", "2.4-maths", "L03.html line 230", "PASS",
    REVERIFIED + "line 230 now says the lesson does not examine a non-monotone supply; it no longer asserts non-uniqueness, so no false claim remains.")
row("E1a-L03-problems", "2.4-maths", "L03.html lines 260-356", "PASS",
    REVERIFIED + "M1: p* = 54/5, Q* = 196/5 (recomputed); M2: Z(12) = -6; M3: n = 4; P1 sign pattern (uses b>0 for slope -b and b>0, s>0 for slope -(b+s)); P2: a <= bc gives p = a/b <= c with zero supply and zero quantity (recomputed); P3: S nondecreasing; E1-E3 counts 110, 1, 30 (110 + 1 + 30 = 141).")
row("E1a-L03-R1-R2", "2.4-maths", "L03.html lines 336-348", "PASS",
    REVERIFIED + "R1: partial of p* wrt a = 1/(b+s) > 0; wrt b = -(a+sc)/(b+s)^2 < 0 (recomputed). R2: c = 0 gives p* = a/(b+s), Q* = sa/(b+s).")
row("E1a-L03-R3-general-existence", "2.4-maths", "L03.html lines 350-355", "PASS",
    REVERIFIED + "Z(0) > 0 > Z(p-bar); IVT (stated as Assumption 1, not proved) gives a zero in (0, p-bar); strict decrease gives uniqueness. Correct; the only hypothesis used beyond the statement is IVT, which is named.")
row("E1a-L03-R3-uniqueness-attribution", "2.9-structure", "L03.html line 354", "PASS",
    REVERIFIED + "the uniqueness argument is stated without an attribution to any source.")
row("E1a-L03-quiz", "2.9-structure", "L03.html lines 378-457", "PASS",
    REVERIFIED + "Quiz numeric keys: 110/7 = 15.714286; 480/7 = 68.571429; S(12) = 50; 196/5 = 39.2; 48/7 = 6.857143 (all recomputed to the displayed digits). Multiple-choice keys: excess supply above p*; zero for a <= bc; positive below p*; market supply n times one firm.")
row("E1a-L03-why-it-matters-positive-quantity", "2.4-maths", "L03.html line 51", "PASS",
    REVERIFIED + "'it shows that the market trades a positive quantity under the condition a > bc': Proposition 1.3 gives Q* = s(p*-c) > 0 under the Setting, which assumes a > bc (line 59). The statement is sufficiency only and makes no claim that a > bc is necessary, which P2 supports for the converse direction.")

# concepts
row("E1a-concept-forward-use", "DAG", "L01.html lines 37, 266; L02.html lines 37, 51, 251; L03.html lines 37, 339", "PASS",
    REVERIFIED + "forward references are lesson-number pointers in prose (L01 line 266 'Lesson 4'; L02 line 251 'Lesson 5'; L03 line 339 'Lesson 4'), not concept links; no concept outside the closure is linked. Named theorems used: extreme value theorem (L01 Assumption 1, stated), Fermat's condition (L01 R2, stated as an M2 fact; M2/L22.html line 63 'Lemma 1.2 (interior maximum, first-order condition)'), intermediate value theorem (L03 R3, stated as Assumption 1), implicit-function theorem (L02 R2, stated as Assumption 1; M2 curriculum concept).")
row("E1a-concept-defined-once", "DAG", "L01.html line 64; L02.html lines 64, 69; L03.html lines 64, 69", "PASS",
    CARRY + "check_dag E1 PASS this round; each dfn with data-concept appears once (utility-maximization, MRS, price-taking, profit-maximization, competitive-equilibrium, excess demand).")
row("E1a-links-and-dag-prereqs", "DAG", "index.html lines 58-64; L01.html line 37; L02.html lines 37, 69; L03.html lines 37, 69", "PASS",
    CARRY + "L01 uses derivative, partial derivative (M2) and natural logarithm (M1); L02 uses derivative (M2); L03 links L02's profit-maximization. All within the closure AC1, S0, S2 and M1/M2/P0.1 used by the hub. check_dag E1 PASS.")

# cards
row("E1a-cards-L01-L03", "2.7-cards", "course/modules/E/E1/cards.json entries E1-c001..E1-c037 (L01 c001-c014, L02 c015-c027, L03 c028-c037)", "FAIL",
    "Checked each card against its lesson text (script ledgers/E1/scripts/E1-a-r4/card_and_term_checks.py). (1) E1-c007 asks for and answers 'x*, y* and u*' with 'x* = 30, y* = 20'; the L01 page no longer contains x* or y* (Example 1.6 line 114 now writes x-bar = 30, y-bar = 20). (2) E1-c013 says 'Tangency holds only at the optimum (Proposition 2.3)'. The current L01 wording (line 283) drops 'only' ('Proposition 2.3 gives the equality at the optimum'), and Proposition 2.3 proves only one direction; 'only' is unproved on the page. (3) E1-c010 uses 'indifference curve', a term that appears nowhere in the L01 page (count 0). Every other card number and claim matched its lesson (card numbers appear in their lessons). Grades: E1-c014, c025, c027, c036 are C with a lab basis; the labs are exact, not simulated, and the findings are finite checks, so C is accepted as a single-run check named by basis.",
    "E1-c007: use x-bar = 30, y-bar = 20 and u* = 600. E1-c013: 'Tangency holds at the optimum (Proposition 2.3)'. E1-c010: replace 'indifference curve' by 'level curve of u' or define the term in L01 first.")
row("E1a-footers", "2.9-structure", "L01.html line 507, L02.html line 498, L03.html line 474 (footers)", "FAIL",
    "The changed footer text 'Each result is proved on the page, proved under a stated assumption, or checked by a lab' holds for every result on the L02 and L03 pages (checked, including the Remark and Problem results). On the L01 page it overclaims while Proposition 1.4 has the proof gap in E1a-L01-prop-1-2-to-1-4, so the footer is not yet true for L01.",
    "Resolved with E1a-L01-prop-1-2-to-1-4 (the footer becomes true once Proposition 1.4's proof is completed). No change needed on L02 or L03.")
row("E1a-references-varian-only", "2.1-citations", "L01.html line 496; L02.html line 487; L03.html line 463", "PASS",
    REVERIFIED + "each page cites only varian2014intermediate (registry 'verified'); no passage locator; no historical attribution (grep for years 1800-2029 in the slice returns none). Architect Q7 satisfied.")

fragment = {
    "unit": "E1",
    "slice": "E1-a",
    "round": 4,
    "verifier": "independent round-4 verifier for E1 slice a (hub index.html, L01-L03 and their lab twins); did not build E1 and shares no context with the builders or with earlier verifiers",
    "pin": "2657ab5",
    "base": "aa3c26c (round-3 pin; delta git diff aa3c26c 2657ab5: index.html lines 34 and 163-167; L01.html many hunks; L02.html lines 51, 251-254, 495; L03.html lines 51, 471; tests/labs/E1/lab-E1-L01-1.py; L02 and L03 twins unchanged)",
    "previous_ledger": "/tmp/fanout-frags/B-E1-a.round3.json",
    "checkout": "/tmp/verifyB4-E1-a (detached at 2657ab5; .venv symlinked)",
    "scratch": "/tmp/e1-v/a4",
    "verified_at": "2026-10-28T00:00:00+00:00",
    "rows": R,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Not a project slice: no student-error mutants are required (brief; architect ruling: lab twins are demonstrations, mutation applies to graders only). None written.",
        "Round-3 PASS rows whose cited subject is byte-identical are carried with the 'Carried from round 3' prefix; rows touching L01, L02 and L03 lines changed in the delta were re-verified from the full page text read this round (every line of L01, L02, L03 and the index lines read).",
        "Round-3 FAIL row E1a-hub-skip-rule re-verified and still FAIL: project.html line 42 unchanged.",
        "Could not check: pytest for the whole unit (not in the slice); Pyodide in-browser timing beyond page_smoke; live numeric check of SEC or market data (none used); the Varian passage (no locator; paywalled book, not read).",
    ],
}
path = f"{ROOT}/ledgers/E1/E1-a.json"
with open(path, "w", encoding="utf-8") as f:
    json.dump(fragment, f, indent=1, ensure_ascii=False)
fails = [r["id"] for r in R if r["status"] != "PASS"]
print("rows", len(R), "fail", len(fails), fails)
