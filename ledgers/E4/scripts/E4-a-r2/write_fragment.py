"""Writes ledgers/E4/E4-a.json (round 2, slice a). Rows reflect the checks run in this checkout at pin 67c47689."""
import json
from datetime import UTC, datetime

S = "scripts/E4-a-r2/"
rows = []


def add(id_, check, location, status, evidence, fix=""):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


# ---- commands and tools
add("E4a-cmd-check_pages-unit", "2.9-structure", "course/modules/E/E4/index.html, L01.html, L02.html, L03.html", "PASS",
    "tools/check_pages.py --unit E4 -> 'check_pages E4: PASS', exit 0 (ledgers/E4/scripts/E4-a-r2/logs/check_pages_unit.txt).")
add("E4a-cmd-check_pages-lessons", "2.9-structure", "L01.html, L02.html, L03.html", "PASS",
    "check_pages.py --unit E4 --page L01 / L02 / L03 each -> 'check_pages E4 Lnn: PASS', exit 0 (logs/check_pages_L01.txt, _L02, _L03).")
add("E4a-cmd-check_dag", "2.9-dag", "all four slice pages", "PASS",
    "tools/check_dag.py --unit E4 -> 'check_dag E4: PASS', exit 0 (logs/check_dag_E4.txt). Linked uses only; unlinked names checked by grep (E4a-dag-outside-closure).")
add("E4a-cmd-run_labs", "2.5-labs", "tests/labs/E4/lab-E4-L01-1.py, lab-E4-L02-1.py, lab-E4-L03-1.py", "PASS",
    "run_labs.py --unit E4 --page L01 / L02 / L03 each -> 'run_labs E4: PASS (1/1)', exit 0 (logs/run_labs_L01.txt, _L02, _L03). The whole-unit run covers L04 to L09 and was not run here.")
add("E4a-lab-twins-alone", "2.5-labs", "tests/labs/E4/lab-E4-L01-1.py, lab-E4-L02-1.py, lab-E4-L03-1.py", "PASS",
    S + "check_twins_embed.py (logs/twins_embed.txt): each twin run as python -I -W error from /tmp with PATH only: exit 0, stderr 0 bytes.")
add("E4a-lab-embed-equality", "2.5-labs", "L01.html, L02.html, L03.html (data-run and pre.expected blocks)", "PASS",
    S + "check_twins_embed.py: L01/L02/L03 page code block equals the twin file (True x3); each pre.expected block equals the twin stdout (True x3). ALL_OK.")
add("E4a-cmd-ruff", "2.5-labs", "tests/labs/E4/lab-E4-L01-1.py, L02-1.py, L03-1.py", "PASS",
    "ruff check -> 'All checks passed!', exit 0; ruff format --check -> '3 files already formatted', exit 0 (logs/ruff_slice.txt).")
add("E4a-cmd-mypy", "2.5-labs", "tests/labs/E4/lab-E4-L01-1.py, L02-1.py, L03-1.py", "PASS",
    "mypy --no-incremental on the three twins -> 'Success: no issues found in 3 source files', exit 0 (logs/mypy_slice.txt).")
add("E4a-cmd-page_smoke", "2.9-smoke", "index.html, L01.html, L02.html, L03.html", "PASS",
    "page_smoke.py --unit E4 --pages index L01 L02 L03, run alone -> 'page_smoke E4: PASS', exit 0; lab times 0.0 s each; boot 1.1 s (logs/page_smoke_slice.txt).")
add("E4a-cmd-pytest", "tooling", "tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py", "PASS",
    "pytest -q on the three modules -> exit 0, no failures (logs/pytest_relevant.txt). The full suite was not run.")
add("E4a-cmd-verify_refs", "2.1-registry", "index.html, L01.html, L02.html, L03.html (data-references)", "PASS",
    "verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0 (logs/verify_refs_offline.txt). The slice cites no registry key: the three data-references lists are empty (L01.html line 512, L02.html line 574, L03.html line 493) and the hub has none, so no live resolution is required of this slice. The live unit run (verify_refs.py --unit E4) needs the network and is left to the unit-level verifier (logs/verify_refs_unit_offline.txt shows the flag is rejected with --unit).")
add("E4a-hours", "2.9-hours", "index.html line 29, 40-43; L01.html, L02.html, L03.html line 2", "PASS",
    "index data-hours-lessons=72, data-hours-project=28, bars 72%/28%; lesson data-hours=8 on L01, L02, L03; 9 x 8 = 72, 72 + 28 = 100, 28 percent of 100 = 28 (rederive_slice_numbers.py, 'hub' checks).")

# ---- numbers
add("E4a-num-hub", "2.2-numbers", "index.html lines 40-43, 68, 73, 87, 96, 101, 110, 115, 120", "PASS",
    S + "rederive_slice_numbers.py (exact Fractions): 9 x 8 = 72; 72 + 28 = 100; 28% of 100 = 28; 7/8 = 87.5%; 6/8 = 75%; placement items: 6, 0.25, 8, 12.5 (= 1/2 x 10 + 1/4 x 30), 4 (= 1/2 x 1 / (1/8)). All OK.")
add("E4a-num-L01", "2.2-numbers", "L01.html lines 92-93, 113-161, 262-281, 320-336, 345-347, 386, 402-404, 447-463, 484-486", "PASS",
    S + "rederive_slice_numbers.py L01 checks (97 OK lines across hub, L01, L02, L03, 0 mismatches; logs/rederive_slice_numbers.txt): V(claim)=340/3, V(other)=56, combination 596/3 both sides, E x = 235/4, value at prices 340/3 = 113.33 to 2 dp, decomposition of Example 1.5, M1 55/3 (18.33), gap 35/6, M2 25, M3 -1/8 = 3V(x)-2V(y) = 33/8-34/8, P3 values 1/4 and 1/3, R2 V(e1)=1/4, V(2e1)=1, Q2 4.25, Q4 3, Q7 0.6.")
add("E4a-num-L02", "2.2-numbers", "L02.html lines 187, 192, 299-337 (lab output), 338, 355-363, 377-393, 429-443, 506-530", "PASS",
    S + "rederive_slice_numbers.py L02 checks: theta = 9/16, 7/16; q* = (1/8, 1/32, 1/16); q*.ebar = 1; demands (9/4, 9/2, 9/4), (7/4, 7/2, 7/4); budget and clearing residuals 0; Walras residual 0; ratios 16/9, 16/7; misconception value of (1,-1,0) = 3/32; wealth of e^1 = 9/16; M1 (1, 2), M2 (3/4, 3/8, 3/2), M3 prices (1/8, 1/8), theta 1/2; Q5 q1* = 0.125. prop28_random_check.py: 300 seeded economies x 400 budget bundles, 0 maximality violations, budget binds at x*.")
add("E4a-num-L03", "2.2-numbers", "L03.html lines 119, 124, 250-261, 301-310, 335-336, 353, 385, 406, 476", "PASS",
    S + "rederive_slice_numbers.py L03 checks: MRS_12 = 4, MRS_13 = 2, MRS_23 = 1/2 for both agents = price ratios 4, 2, 1/2; M1 MRS 2; M2 demand (3/2, 3) and MRS 2; R2 derivatives 1/12 and 1/4; endowment MRS 8/3 (agent 1) and 8 (agent 2); grid 125 points, 0 improvements at equilibrium, 2 at endowment, first witness (2,4,3)/(2,4,1) with float margins 0.072 > 1e-12. Row E4a-L03-state-labels covers the 0-based labels in line 406.")

# ---- mathematics
add("E4a-math-L01", "2.4-mathematics", "L01.html lines 77-151, 286-287, 358-361, 393-412", "PASS",
    "Prop 1.4 (sum over one nonzero term), Prop 1.7 (induction on finite sums from A2, finiteness from A1), Prop 1.8 (take x = e_s), Prop 1.10 both directions (E e_s = pi_s), P2 (a=0, b=0 and a=-1, b=0 in A2), R3 both directions, R2 counterexample (V(2e1)=1 vs 2V(e1)=1/2). Hypotheses cited by number (A1, A2). Continuity remark handled in E4a-L01-continuity-necessity.")
add("E4a-math-L02", "2.4-mathematics", "L02.html lines 99-178, 451-455", "PASS",
    "Lemma 2.4 test bundle z = (w/(2 q.iota)) iota is in B(q) with finite utility (A4). Corollary 2.7 uses q_s > 0. Prop 2.8: tangent-line inequality for ln, pi_s/x*_s = q_s/w, the chain of inequalities, equality case forces x = x* (pi_s > 0). Prop 2.9: theta_1 + theta_2 = 1, q*.ebar = 1, w_i = theta_i > 0, x^{i*} = theta_i ebar_s, clearing. R1 sums over I agents (no two-agent property used). Remark 2.10 scale invariance. Prop 2.5's gap is in E4a-wi-positive, not here.")
add("E4a-math-L03", "2.4-mathematics", "L03.html lines 91-101 (Step 1 to 3 of Prop 3.4 (a)), 117-119, 335-336, 342, 378, 385-392", "PASS",
    "Steps 1 and 2 re-derived line by line (strictly higher utility than the demand implies q.y > w; a weak gain implies q.y >= w, using positive y, A4 and A1); Step 3 gives q.(y1+y2) > q.ebar, but y1+y2 = ebar by feasibility, a contradiction. Example 3.6 MRS values re-derived. P2 (MRS = pi_s ebar_t / (pi_t ebar_s) for both agents). R1 free-disposal argument valid. R2 derivatives and feasibility checked. The w_i > 0 hypothesis used in Step 3 is the gap in E4a-wi-positive, not here.")
add("E4a-math-L03-b-uprime", "2.4-mathematics", "L03.html line 71 (Definition 3.3), line 109 (proof of Prop 3.4 (b))", "FAIL",
    "The proof of (b) divides G = 0 by pi_t u_i'(x_t)/q*_t, and Definition 3.3 divides by the same derivative, but neither line shows u_i'(x_t) != 0. A4 gives it: u_i' >= 0 by strict monotonicity, u_i' is nonincreasing by concavity, and if u_i'(x0) = 0 then u_i' = 0 on (x0, inf), so u_i is constant there, contradicting strict monotonicity. The page never says this.",
    "Add before the division in the proof of (b): 'u_i'(x_t) > 0 for x_t > 0, since u_i' is nonnegative and nonincreasing and u_i' = 0 at some point would force u_i' = 0 to its right, contradicting strict monotonicity.'")
add("E4a-assumptions", "2.4-mathematics", "L01.html lines 61, 99; L02.html lines 58, 63, 93; L03.html line 55", "PASS",
    "A1 (finite, strictly positive states), A2 (linear valuation), A3 (strictly positive endowments), A4 (utility on (0,inf): increasing, concave, differentiable; the -inf convention), A5 (existence, a hypothesis) are numbered and stated before use; every Proposition cites its Assumptions by number (for example Prop 1.4 'Assume A1', Prop 2.5 'Assume A1, A3 and A4', Prop 3.4 'Assume A1, A3 and A4').")
add("E4a-existence-scope", "2.4-mathematics", "L02.html lines 51, 94, 182, 345; L03.html lines 268", "PASS",
    "Existence is A5 and never proved (L02 line 94); Remark 2.10 says Prop 2.9 does not prove uniqueness; L02 line 345 and L03 line 268 name A5 as the hypothesis; L01 canon-breaks states its own limits.")
add("E4a-A2-nonlinear-sources", "2.4-mathematics", "L01.html line 104", "PASS",
    "'A2 excludes quantity discounts, bid-ask spreads and price impact, because each of those makes V nonlinear': a conceptual statement with no number, re-read this round. A quantity discount makes V(2x) != 2V(x) (R2 gives the size case explicitly); the other two are conceptual, and the sentence says A2 is an assumption that the lesson does not derive.")
add("E4a-scope-words", "2.9-prose", "index.html, L01.html, L02.html, L03.html", "PASS",
    "grep of always|never|only|any|same|exactly|in general|drives|all over the four pages (about 90 hits, read in context): each universal claim is backed by a derivation, a finite check labelled as such, or an explicit hypothesis (for example 'every claim' with A1 in Prop 1.4; 'R1 extends Prop 2.9 ... with the same proof' with the R1 solution at L02 line 454; 'the lab checks these identities for these four states and these prices', L01 line 281). No unsupported universal found.")

# ---- structure, prose, cards, hub
add("E4a-struct-hub", "2.9-structure", "index.html lines 29-158", "PASS",
    "8 objectives with measurable verbs (lines 49-58); prerequisites E2, E3, M7 (line 35) match curriculum.json; placement diagnostic with 8 items: 6 prerequisite items and 2 items marked data-skill (lines 112, 117); data-mastery 0.8 and the 7-of-8 arithmetic (line 68); lesson map of 9 cards (lines 128-138); project ladder with 4 rungs (lines 144-149); data status (lines 153-156).")
add("E4a-struct-lessons", "2.9-structure", "L01.html, L02.html, L03.html", "PASS",
    S + "rederive_slice_numbers.py and read: why-it-matters 105, 102 and 110 words (limit 120); numbered core sections; inline lab before 'Where the canon breaks'; canon-breaks; 3 misconceptions each; 3 problems in each of Mechanics, Proof, Empirical, Research, each with a details.solution; key-results table; 9 quiz items each; references with empty data-references; lesson-nav to the adjacent lessons.")
add("E4a-quiz-items", "2.9-structure", "L01.html lines 437-505; L02.html lines 495-567; L03.html lines 418-486", "PASS",
    "27 quiz items read. Keys recomputed: L01 (5,7) gives 7; 4.25; V(2x)=2V(x); E x = 3; security property; A1; 0.6; r = q; nonlinearity from size discount. L02 2; 0.125; q.z = 0; Lemma 2.4; w_i as theta_i; unchanged under scaling; best affordable bundle; Prop 2.9 existence scope. L03 part (a) statement; MRS 2; Pareto improvement definition; differentiability; 2; 4; Pareto efficiency; 4; proof step for strict monotonicity. Each explanation matches its lesson.")
add("E4a-banned-phrases", "2.9-prose", "index.html, L01.html, L02.html, L03.html", "PASS",
    "check_pages.py banned-string check PASS on every page; grep for TODO, TBD, lorem, 'for brevity', 'beyond the scope', 'it is important to note', 'obviously', 'clearly', 'studies show', 'well known', 'experts agree', 'left as an exercise', 'details omitted': no hits. '...' appears only inside Python code blocks (L01 line 181; L02 lines 219-239; L03 lines 151-173).")
add("E4a-process-words", "2.9-prose", "index.html, L01.html to L03.html, lab-E4-L01-1 to L03-1 (twins)", "PASS",
    "grep for build, builder, round, verifier, REQUEST, planner, architect, fixer, ruling, plan, unit report: hits only 'rebuilds' (L01.html line 160) and 'rounding' (L02.html line 198; twin L02 line 6). These are ordinary words, not process words.")
add("E4a-hub-cards-h1", "2.9-structure", "index.html lines 129, 130, 131, 134, 135, 136, 137", "PASS",
    "Card titles equal the <h1> of the lesson exactly: L01 'Arrow–Debreu securities and state-contingent payoffs' (L01.html line 35); L02 'Arrow–Debreu equilibrium' (L02.html line 35); L03 'The first welfare theorem' (L03.html line 35); L06 'Noisy rational-expectations equilibrium'; L07 'Price informativeness'; L08 'The Grossman–Stiglitz Paradox'; L09 'The No-Trade Theorem' (the L06 to L09 h1 values read with grep '<h1>'). L04 and L05 are in a separate row.")
add("E4a-hub-cards-h1-L04-L05", "2.9-structure", "index.html line 132 (L04 card), line 133 (L05 card); L04.html and L05.html <h1>", "FAIL",
    "Hub card L04 reads 'Complete and incomplete markets' but L04.html's h1 reads 'Complete and Incomplete Markets'. Hub card L05 reads 'Rational-expectations equilibrium' but L05.html's h1 reads 'Rational-Expectations Equilibrium'. Plan §2.2 requires hub lesson titles to match each <h1> at integration.",
    "Make the card text equal the h1 exactly: either set index.html line 132 to 'Complete and Incomplete Markets' and line 133 to 'Rational-Expectations Equilibrium', or change the h1 in L04.html and L05.html to the card text. One choice, applied to both pages.")
add("E4a-hub-prereq-unlock", "2.9-structure", "index.html lines 35-36", "PASS",
    "curriculum.json: E4 prereqs ['E2','E3','M7'] and hours 100; the four modules that list E4 as a prerequisite are AP1 (M6, AP2, FC1, FC2, M8, E4), AP6 (AP5, E4), MS1 (E4, S1), SR1 (BK1, E4). Titles on the hub match curriculum.json: 'Game Theory & Information Economics', 'Decision Theory Under Risk & Ambiguity', 'Optimization', 'No-Arbitrage & the Stochastic Discount Factor', 'Intermediary & Institutional Asset Pricing', 'Microstructure Theory', 'Runs, Liquidity & Fire Sales'.")
add("E4a-hub-introduces", "2.9-structure", "L01.html line 38, 74; L02.html line 38, 89; L03.html line 38, 78", "PASS",
    "Each lesson's 'Introduces' names its one concept (arrow-debreu-security, arrow-debreu-equilibrium, first-welfare-theorem) and that concept has exactly one <dfn data-concept> in the lesson (lines 74, 89, 78).")
add("E4a-hub-placement-explain", "2.9-structure", "index.html lines 78, 87, 96, 101, 110, 115, 120", "PASS",
    "Explanations re-read against their lessons. Item 2 says Lesson 2 uses the derivative of ln 'in the first-order condition of the logarithmic demand': L02 Lab 2 Part D is the 'first-order ratio' (L02.html line 207, twin line 15) and L02 line 443 says 'as the first-order condition predicts', and Prop 2.8 uses the tangent-line inequality for ln, which rests on the same derivative. Item 4 cites Definition 2.2 (L02 line 84). Item 7 cites Lesson 1 Proposition 1.7 (L01 line 113). Item 8 cites Proposition 2.8 (L02 line 143).")
add("E4a-dag-outside-closure", "2.9-dag", "index.html, L01.html, L02.html, L03.html", "PASS",
    "Plain-text grep (script grep_terms.py) for bayes, posterior, state price, stochastic discount, martingale, efficient markets, informationally efficient, CARA, common knowledge, two-fund, diagnostic, fixed point, intermediate value, banach: none in lesson text except the hub card of L09 ('posteriors as conditional probabilities', index.html line 137), which is plain prose with no link. 'Efficient' appears only as Pareto efficiency (linked E1 concept). 'Arrow–Debreu security price vector' is used; 'state price' is not.")
add("E4a-links-earlier-lessons", "2.9-dag", "L02.html line 37, 84, 89; L03.html line 37, 64", "PASS",
    "L02 links L01.html#def-arrow-debreu-security (defined at L01.html line 74); L03 links L02.html#def-arrow-debreu-equilibrium (L02.html line 89) and L01.html#def-arrow-debreu-security. No link points to a later lesson. Prerequisite concept links use concepts.html anchors, and check_dag PASS confirms the linked uses.")
add("E4a-define-before-use", "2.9-prose", "L02.html line 51 (Walras' law, before its <dfn> at line 110); L03.html line 51 (first welfare theorem, dfn at line 78; marginal rate of substitution, Definition 3.3 at line 68-69)", "FAIL",
    "Plan §2.1 item 5 requires each unit concept to be defined 'and never before it', and terms outside the nine to be defined in prose 'at first use'. L02 line 51 names 'Walras' law (Proposition 2.5)' in the why-it-matters paragraph before the term is defined at line 110. L03 line 51 names 'The first welfare theorem' (a unit concept whose dfn is at line 78) and 'the marginal rate of substitution (Definition 3.3)' before either is defined. The forward pointers are not definitions. 'interior' is defined inline at L03 line 51 (its dfn is at first use) and passes.",
    "L02 line 51: define Walras' law in prose at first use with a plain <dfn> (no data-concept), or drop the term from line 51. L03 line 51: do not name the first welfare theorem or the marginal rate of substitution before their definitions; for example 'The efficiency result proved below (Proposition 3.4) says...' and 'the rate at which an agent trades one state for another'.")
add("E4a-define-interior", "2.9-prose", "L03.html line 51", "PASS",
    "'interior' is defined with a plain <dfn> at its first use (L03 line 51) and is used later only in that defined sense (lines 271, 310, 451).")

# ---- labs (statements)
add("E4a-lab-hypothesis-before-output", "2.5-labs", "L01.html line 160 vs 262; L02.html line 192 vs 313; L03.html line 124 vs 250", "PASS",
    "Each hypothesis paragraph precedes its pre.expected block in the page order.")
add("E4a-lab-L01-statements", "2.5-labs", "L01.html lines 160, 281; L01.html code lines 219-261 (twin lines 59-101)", "PASS",
    "Hypothesis numbers 340/3, 56, 2 and -1/2 combination, 235/4, and the two ValueError rejections (negative entry; entries summing to 9/8, which the 'short' vector sums to: 1/8+3/8+3/8+1/4 = 9/8) match printed lines 270-280. Interpretation (line 281) matches. Misconception 3 claim 'checks its unequal probabilities once, at the start of main()' matches code line 222 (twin line 62).")
add("E4a-lab-L02-statements", "2.5-labs", "L02.html lines 192, 193-212, 338; tests/labs/E4/lab-E4-L02-1.py", "PASS",
    "Hypothesis (aggregate (4,8,4); shares 9/16, 7/16; prices; demands; ratios 16/9 and 16/7 'one over the agent's wealth'; Part E with re-valued wealth; Part F zero-endowment rejection) matches printed lines 314-337. Interpretation (line 338): five residuals (two budget, three clearing) plus Walras, all 0 (lines 323-329); Part E explained with wealth fixed (factor 3). Docstring lines 193-212 match the code and output.")
add("E4a-lab-L03-interpretation", "2.5-labs", "L03.html lines 124, 261; tests/labs/E4/lab-E4-L03-1.py lines 1-20", "PASS",
    "Hypothesis: MRS 4, 2, 1/2 equal to price ratios (lines 252-254), grid of 125 with {0,1/4,1/2,3/4,1}, zero improvements at the equilibrium and at least one at the endowment (lines 257-259), TOL 1e-12. Interpretation (line 261): 0 of 125 and 2 of 125; first witness (2,4,3)/(2,4,1) (line 260). The docstring's note that printed 'states 1 2' is the code pair (0,1) matches line 224 (left + 1).")
add("E4a-lab-runtime-rng-stdlib", "2.5-labs", "tests/labs/E4/lab-E4-L01-1.py, L02-1.py, L03-1.py", "PASS",
    "Imports: __future__, fractions (L01, L02); math, fractions, itertools (L03). No random import and no draw in any twin. main() called at module top level with no __name__ guard. page_smoke lab times 0.0 s each (under 10 s).")
add("E4a-simulated-data", "2.8-data", "index.html lines 38, 155; L01-L03 labs", "PASS",
    "No data-files attribute in the slice and no dataset is named. Every lab is exact arithmetic on fixed inputs with no random draws; no SIMULATED label is needed in this slice, and none is claimed beyond the 'no data' statements.")
add("E4a-figures", "2.8-data", "index.html, L01.html, L02.html, L03.html", "PASS",
    "No svg, figure or data-figures element in the four pages (grep).")
add("E4a-mutants", "2.6-mutation", "tests/labs/E4 (no grader in slice a)", "PASS",
    "The slice has no grader. Lab twins are demonstrations, and mutation testing applies to project graders only (LAB MUTANTS ruling). No mutant claimed for slice a.")

# ---- round-1 rows re-verified
add("E4a-L01-misc2-partA", "2.2-claims", "L01.html line 307; L01.html code line 222 (twin line 62) before the Part A print at code line 224", "PASS",
    "Round-1 FAIL, now fixed. Misconception 2 says 'Lab 1 checks its unequal probabilities once, at the start of main(), before Part A'. Code line 222 (twin line 62) calls check_probabilities(STATE_PROBABILITIES) inside main() before the Part A print at code line 224.")
add("E4a-term-additive", "2.4-mathematics", "index.html lines 50, 129; L01.html lines 7, 51", "PASS",
    "Round-1 FAIL, now fixed: 'additive' does not appear in the four pages (grep). The text now says 'linear valuation of A2' (index line 50, 129; L01 lines 7, 51), which is the property the lesson assumes (A2, L01 line 102).")
add("E4a-L01-R2-title", "2.2-claims", "L01.html line 401 (title), lines 402-404 (solution)", "PASS",
    "Round-1 FAIL, now fixed. Title 'A size effect breaks linearity'. The example V(x) = (sum q_s x_s)^2 gives V(2e1) = 1 = 4 V(e1), a size premium, which matches the title and the canon-breaks text (line 288: 'a quantity discount or a size premium').")
add("E4a-L01-continuity-necessity", "2.4-mathematics", "L01.html line 287 (canon-breaks), line 397 (R1 solution)", "PASS",
    "Round-1 FAIL, reworded. Line 287 now says the step 'is not justified without an extra condition on V' and 'This lesson does not state or verify a sufficient condition'; line 397 says the step is 'not justified ... without an extra condition' and offers continuity along partial sums as one example. Neither line asserts that the formula is false without the condition. Judgement: PASS. The phrase 'the step that fails' in line 397 refers to the application of A2 to an infinite sum, which the proof cannot perform.")
add("E4a-L01-P3-title", "2.9-prose", "L01.html line 358 (title of P3), lines 359-361 (solution)", "FAIL",
    "P3 is titled 'A counterexample to the converse with two states', but the converse of Proposition 1.10's (b) => (a) is (a) => (b), and Proposition 1.10 proves (a) => (b), so no counterexample to that converse exists. The solution (lines 361) shows that (a) fails when q != pi, which is the contrapositive of (a) => (b), not a counterexample to it.",
    "Retitle P3, for example 'P3 · Prices that differ from probabilities, two states', and add: 'This is the contrapositive of Proposition 1.10.'")
add("E4a-L02-residual-count", "2.2-claims", "L02.html line 338; expected block lines 322-329", "PASS",
    "Round-1 FAIL, now fixed. The interpretation says 'five budget and market-clearing residuals (two budget, three market-clearing) and the Walras residual are 0 exactly'. Printed output lines 323, 325 (two budget_residual lines), 326-328 (three clearing lines), 329 (walras_law_residual 0).")
add("E4a-L02-partE-wealth", "2.2-claims", "L02.html lines 182, 192, 208, 298-302 (code block Part E), 338, 443; twin docstring lines 16-17", "PASS",
    "Round-1 FAIL, now fixed. Every statement that demand is unchanged under price scaling now re-values wealth at the new prices (lines 192, 208, 338, 443; Remark 2.10 line 182 states the (lambda q, lambda w) invariance). Re-derivation: with wealth fixed the demand falls by 3 (rederive_slice_numbers.py, 'L02 part E' checks).")
add("E4a-L02-partF-docstring", "2.5-labs", "tests/labs/E4/lab-E4-L02-1.py lines 16-18 (docstring; Part F at line 18) and line 112 (Part F print); L02.html lines 208-210", "PASS",
    "Round-1 FAIL, now fixed. The docstring now says 'an economy with a non-positive (zero) endowment entry is rejected with a ValueError'. The Part F input contains Fraction(0), and check_economy raises for entries <= 0. Printed message line 337 matches.")
add("E4a-L02-uniqueness-z", "2.4-mathematics", "L02.html lines 84, 89, 148", "PASS",
    "Round-1 FAIL, now reworded. Definition 2.2 defines a demand as a maximizer in the budget set; Definition 2.3 now says 'x^i(q) denotes the demand chosen for agent i at q' and z(q) is computed 'from those choices'. Uniqueness is proved only for the logarithmic case (Prop 2.8, line 148). The convention is explicit. Note, not a finding: the sentence that markets clear 'exactly when z(q*) = 0' presumes the chosen demands at q* are the equilibrium bundles; stating that would remove any doubt.")
add("E4a-L02-CRRA-no-closed-form", "2.4-mathematics", "L02.html line 346 (canon-breaks)", "PASS",
    "Round-1 FAIL, now fixed: the text says the formula 'need not give the demand' and that a power utility with gamma = 2 satisfies A4 and its demand is not derived. Checked: u(x) = -1/x is strictly increasing (u' = 1/x^2 > 0), strictly concave (u'' = -2/x^3 < 0) and differentiable on (0, inf). The notation of that sentence is in E4a-notation-gamma.")
add("E4a-L02-A4-finite-zero", "2.4-mathematics", "L02.html line 68", "PASS",
    "Round-1 FAIL, now fixed: the sentence now says 'The display in A4 sets U_i = -inf at a zero entry, so the value of u_i at zero never enters; no result below uses it.' It no longer asserts that A4 excludes utilities finite at zero.")
add("E4a-L03-remark36", "2.9-prose", "L03.html line 59; research problem R1 at line 375", "PASS",
    "Round-1 FAIL, now fixed: Definition 3.1 says 'Research problem R1 treats the case with free disposal', and R1 (line 375) does treat it (solution at line 378, re-derived). No 'Remark 3.6' is referenced in the slice (grep).")
add("E4a-L03-state-labels", "2.9-prose", "L03.html line 406 (key-results row); round-1 locations 119, 302, 384, 473 and L02.html 355 are now consistent", "FAIL",
    "The key-results row reads 'MRS_01 = 4, MRS_02 = 2, MRS_12 = 1/2' (0-based labels). Example 3.6 (line 119) numbers the states 1, 2, 3 and gives MRS_12 = 4, MRS_13 = 2, MRS_23 = 1/2, and Lab 3 prints 'states 1 2', 'states 1 3', 'states 2 3' (L03.html code lines 132-134, twin lines 8-10; output lines 252-254). The other round-1 locations are fixed.",
    "Change line 406 to 'MRS_12 = 4, MRS_13 = 2, MRS_23 = 1/2' to match Example 3.6 and the lab output.")
add("E4a-L03-R3-cannot", "2.9-prose", "L03.html lines 389-393", "PASS",
    "Round-1 FAIL, now fixed. The prompt asks why the proof of (b) does not extend to a boundary allocation. The solution argues that a move lowering a zero entry leaves the orthant and the utility is -inf there, so the derivative at 0 does not exist for that move. No 'cannot be stated' wording remains. Re-read and judged PASS.")
add("E4a-L03-lab3-because", "2.5-labs", "L03.html line 124", "PASS",
    "Round-1 FAIL, now fixed. The hypothesis now says 'At the endowment the search should find at least one improvement on the grid. The lesson gives no proof of this prediction, and the printed count is the evidence.' The unsupported 'because' reason is gone.")
add("E4a-L03-M2-scope", "2.9-prose", "L03.html line 310 (solution to M2)", "FAIL",
    "The solution says the marginal rate equals the price ratio 'as Proposition 3.4 (b) predicts for an interior optimum'. Proposition 3.4 (b) is stated for Arrow–Debreu equilibrium bundles (line 82), while M2 is one agent's logarithmic demand at given prices q = (2, 1). The rate check (2 = q1/q2) is correct; the attribution to Prop 3.4 (b) is outside its stated hypothesis.",
    "Replace with 'as the argument in the proof of Proposition 3.4 (b) gives for any demand at q, since it uses only the demand property' (or state the equilibrium hypothesis).")
add("E4a-wi-positive", "2.4-mathematics", "L02.html line 120 (proof of Prop 2.5); L03.html line 93 (proof of Prop 3.4 (a))", "FAIL",
    "Both proofs invoke Lemma 2.4 for strict positivity, which the lemma states under w_i > 0 (L02 line 101). Neither proof establishes w_i > 0. It holds (w_i = q.e^i > 0 by A3 and q in (0,inf)^S), but the page never says so, so the Lemma's hypothesis is unchecked at both points.",
    "In both proofs, add before the Lemma call: 'w_i = q.e^i > 0, because q is strictly positive and e^i is strictly positive by A3.'")
add("E4a-notation-mathbf1", "2.2-notation", "index.html; L01.html lines 345-347, 486; L02.html lines 106, 120, 525; L03.html line 95", "PASS",
    "Round-1 FAIL, now fixed: no \\mathbf{1} anywhere in the four pages or the three twins (grep). The vector of ones is \\iota (L01 345, L02 106, L03 95). \\indic (registered as \\mathbf{1}, notation.json) is not used.")
add("E4a-notation-registered", "2.2-notation", "index.html, L01.html, L02.html, L03.html", "PASS",
    "Only registered macros used in the slice: \\R (10 uses) and \\E (10 uses) per notation.json; no raw \\mathbb; no T, Phi, gamma_3, gamma_4, R^ast, R^{e ast} or \\mathbb{Q} in any slice page (grep). Plain \\gamma is in E4a-notation-gamma; lambda in E4a-notation-lambda.")
add("E4a-notation-lambda", "2.2-notation", "index.html lines 81, 83, 84 (quiz); L02.html lines 182, 409, 411, 542, 545-548", "FAIL",
    "Plan §2.3 binds lambda to the informed fraction (E4's local symbol, used in L08). Here lambda is a scale factor in L02 (Remark 2.10 line 182; P2 lines 409-411; quiz Q7 lines 542-548) and a Lagrange multiplier in the hub's placement item 3 (index lines 81-84). The same symbol then has three meanings in one unit.",
    "Rename the scale factor to kappa in L02 (Remark 2.10, P2, Q7) and the hub multiplier to nu (index lines 81, 83, 84). Reserve lambda for the informed fraction in L08.")
add("E4a-notation-gamma", "2.2-notation", "L02.html line 346 (canon-breaks)", "FAIL",
    "Plan §2.3 states 'Plain \\gamma is not used either' (in the row for gamma_3 and gamma_4). L02 line 346 writes 'a power utility x^{1-gamma}/(1-gamma) with gamma = 2'.",
    "Drop the symbol: write 'the utility -1/x, which satisfies A4', or use a letter not listed in plan §2.3.")
add("E4a-attribution", "2.1-citations", "index.html, L01.html, L02.html, L03.html", "PASS",
    "No data-cite; data-references lists empty; no author names or bibliographic data. 'Grossman–Stiglitz' appears only as the name of the paradox (index lines 7, 33, 56, 136), with no paper attributed. Walras' law is an eponym, not a citation. Muth, Milgrom, Mas-Colell and Stiglitz do not appear.")

fails = [r for r in rows if r["status"] != "PASS"]
frag = {
    "unit": "E4",
    "slice": "a",
    "round": 2,
    "verifier": "Haiku independent verifier, E4-a round 2 (did not build E4; no shared context with the builders)",
    "pin": "67c47689c49435bc0e6639e3de4feded5eefdd64",
    "base": "1c1645f3b00eada2fb54d39c86d5d949e15b4fbc (round-1 pin). Delta read hunk by hunk for index.html, L01, L02, L03, tests/labs/E4/lab-E4-L02-1.py and lab-E4-L03-1.py; every row re-verified this round.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE2-E4-a (detached at 67c47689; .venv symlinked)",
    "scratch": "/tmp only for twin runs (cwd /tmp). Kept scripts and logs: ledgers/E4/scripts/E4-a-r2/ (grep_terms.py, check_twins_embed.py, rederive_slice_numbers.py, prop28_random_check.py, write_fragment.py, logs/).",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice: course/modules/E/E4/index.html (hub, 161 lines), L01.html (524 lines), L02.html (586 lines), L03.html (506 lines) and twins tests/labs/E4/lab-E4-L01-1.py, lab-E4-L02-1.py, lab-E4-L03-1.py. All read in full, line by line, in this round.",
        "Notation (not a FAIL, for the slice d and e builders): plan §2.3 gives s as the signal, but s is the state index throughout L01 to L03 (for example Definition 1.3). L06 and L07 must not reuse s for the signal. The pages also use q for security prices where the plan's local list names p; no collision, but L07 must use one symbol for price consistently.",
        "The hub placement arithmetic, the derivative-of-ln claim in placement item 2 and the four downstream modules were checked against curriculum.json, not against any document other than the curriculum.",
        "The L02 Definition 2.3 convention (x^i(q) is the chosen demand) is recorded as PASS with a note. A stated equality of chosen demands and equilibrium bundles at q* would remove any doubt.",
        "Round-1 FAIL rows that are now fixed and re-verified: E4a-L01-misc2-partA, E4a-term-additive, E4a-L01-R2-title, E4a-L01-continuity-necessity (reworded; judged PASS), E4a-L02-residual-count, E4a-L02-partE-wealth, E4a-L02-partF-docstring, E4a-L02-uniqueness-z (judged PASS), E4a-L02-CRRA-no-closed-form, E4a-L02-A4-finite-zero, E4a-L03-remark36, E4a-L03-R3-cannot, E4a-L03-lab3-because, E4a-notation-mathbf1. Round-1 rows that remain FAIL under new locators: E4a-define-before-use, E4a-L03-state-labels (now only key-results row 406).",
    ],
    "summary": {
        "rows": len(rows),
        "pass": sum(1 for r in rows if r["status"] == "PASS"),
        "fail": sum(1 for r in rows if r["status"] == "FAIL"),
        "unverifiable": sum(1 for r in rows if r["status"] == "UNVERIFIABLE"),
        "mutants_killed": 0,
        "mutants": 0,
    },
}
out = "/Users/billyribeiro/.fanout/wt/verifyE2-E4-a/ledgers/E4/E4-a.json"
with open(out, "w", encoding="utf-8") as fh:
    json.dump(frag, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print("rows", len(rows), "fails", len(fails), [r["id"] for r in fails])
