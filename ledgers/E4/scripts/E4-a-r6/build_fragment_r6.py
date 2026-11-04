"""E4 slice a round 6: writes the fragment ledgers/E4/E4-a.json from the rows verified in this round.

Usage: python -I build_fragment_r6.py <checkout-root>. Evidence strings cite the scripts and outputs kept in
ledgers/E4/scripts/E4-a-r6/ and the page locators read this round. Every row was checked this round; none is carried.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
P = "PASS"
F = "FAIL"
rows: list[dict[str, str]] = []


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str = "") -> None:
    item = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != P:
        item["fix"] = fix
    rows.append(item)


S = "ledgers/E4/scripts/E4-a-r6/"

# commands and gates
row("E4a-r6-cmd-check_pages", "2.9-structure", "index.html, L01.html, L02.html, L03.html", P,
    "tools/check_pages.py --unit E4 printed 'check_pages E4: PASS' (exit 0), " + S + "check_pages_E4.out.")
row("E4a-r6-cmd-check_dag", "2.9-DAG", "index.html, L01-L03", P,
    "tools/check_dag.py --all printed 'check_dag E4: PASS' (exit 0), " + S + "check_dag.out.")
row("E4a-r6-cmd-run_labs", "2.5-labs", "tests/labs/E4/lab-E4-L01-1.py, L02-1.py, L03-1.py", P,
    "tools/run_labs.py --unit E4 printed 'run_labs E4: PASS (12/12)' (exit 0), " + S + "run_labs_E4.out.")
row("E4a-r6-cmd-page_smoke", "2.9-smoke", "index.html, L01.html, L02.html, L03.html", P,
    "tools/page_smoke.py --unit E4 --pages index.html L01.html L02.html L03.html printed 'page_smoke E4: PASS' (exit 0), " + S + "page_smoke_E4_abc.out.")
row("E4a-r6-cmd-twins-alone", "2.5-labs", "tests/labs/E4/lab-E4-L01-1.py, L02-1.py, L03-1.py", P,
    "From cwd /tmp, python -I -W error on each twin by absolute path: exit 0 for L01, L02, L03; stderr empty (twin-L01/02/03.err); stdout in twin-L0n.out.")
row("E4a-r6-cmd-twin-embed", "2.5-labs", "L01.html, L02.html, L03.html lab sections (data-run code, pre.expected)", P,
    S + "check_twins_embed.py output: code==twin True and expected==twin output True for L01, L02, L03; ALL_OK.")
row("E4a-r6-cmd-ruff", "tooling", "tests/labs/E4 twins L01-L03", P,
    "ruff check: All checks passed; ruff format --check: 3 files already formatted (" + S + "ruff_twins.out).")
row("E4a-r6-cmd-mypy", "tooling", "tests/labs/E4 twins L01-L03", P,
    "mypy --no-incremental on the three twins: Success, no issues found in 3 source files (" + S + "mypy_twins.out).")
row("E4a-r6-cmd-pytest", "tooling", "tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py", P,
    "python -m pytest -q on the three files: all dots, exit 0 (" + S + "pytest_relevant.out).")
row("E4a-r6-cmd-verify_refs", "2.1-citations", "index.html, L01-L03 (data-references)", P,
    "tools/verify_refs.py --offline: offline integrity 560 entries, 0 problems, exit 0 (" + S + "verify_refs_offline.out). The slice cites no registry key (empty ol data-references on L01-L03; no data-references on the hub), so no live resolution is owed for this slice.")
row("E4a-r6-cmd-check_projects", "tooling", "course/modules/E/E4/project.html (outside slice)", P,
    "tools/check_projects.py --all exit 0 (run for the gate only; project content belongs to another slice).")

# structure
row("E4a-r6-struct-lesson-order", "2.9-structure", "L01.html, L02.html, L03.html", P,
    "Section order read in each file: why-it-matters, numbered sections with Definition/Proposition/Proof/Example/Remark blocks, lab section before canon-breaks, misconceptions, problem set (Mechanics, Proof, Empirical, Research), key-results table, retrieval quiz, references, lesson nav. Matches BUILDER_RULES 4.2.")
row("E4a-r6-struct-counts", "2.9-structure", "L01-L03 misconceptions, problems, quiz", P,
    "structure_counts_r6.py: each lesson has 3 misconceptions, 3 problems in each of 4 tiers (12 problems), 9 quiz items with 9 explanations (range 8-15 met). " + S + "structure_counts_r6.out.")
row("E4a-r6-struct-why-words", "2.9-structure", "L01 line 51, L02 line 51, L03 line 51", P,
    "why-it-matters word counts (script) 107, 117, 120; all at most 120 words (BUILDER_RULES 4.2 item 1).")
row("E4a-r6-struct-solution-words", "2.9-structure", "L01-L03 details.solution blocks", P,
    "Every solution has at least 20 words (script; the shortest is 20 words in L03 R3). " + S + "structure_counts_r6.out.")
row("E4a-r6-hours-arith", "2.9-structure", "index.html lines 29, 40-43; L01-L03 line 2 and eyebrow", P,
    "index data-hours-lessons=72, data-hours-project=28, sum 100; curriculum.json E4 hours 100; 9 lessons x 8 h = 72 (index line 139 and card kickers L01-L09 each 8 h); each lesson data-hours=8 and eyebrow '8 study hours'; split bars 72% and 28%.")
row("E4a-r6-hub-placement", "2.2-numbers / 2.9-prose", "index.html lines 66-135", P,
    "Eight placement items: six non-skill, two data-skill (items 7 and 8). Mastery 0.8. Numeric answers 6 (0x1/4+8x3/4) and 8 ((1/2)x0 + (1/2)x16) re-derived. 7/8 = 87.5 percent and 6/8 = 75 percent re-derived; 80 percent of 8 = 6.4 so seven correct is needed. Rung-1 bracket: gap signs at 0, 1/2, 1 give keep [0,1/2]. Rung-2 gap G = -e^{ac}F_I + F_U re-derived. Explanations read against lessons (E2 Lesson 3 adverse selection, E2 Lesson 4 signaling, E1 Definition 2.2 price-taking, E3 expected utility).")
row("E4a-r6-hub-titles", "2.9-structure", "index.html lines 129-149; L01-L09 h1", P,
    "Hub card titles equal each lesson h1 for L01-L09 (grep comparison in this round).")
row("E4a-r6-hub-unlocks", "2.9-DAG", "index.html line 36", P,
    "curriculum prereqs containing E4: AP1, AP6, MS1, SR1 (complete list over the whole curriculum.json); titles in the hub match the curriculum titles.")
row("E4a-r6-hub-prereq-titles", "2.9-prose", "index.html line 35", P,
    "E2 'Game Theory & Information Economics', E3 'Decision Theory Under Risk & Ambiguity', M7 'Optimization' match curriculum.json.")
row("E4a-r6-hub-KKT-claim", "2.9-DAG / 2.4-math (round-5 FAIL re-verified)", "index.html line 63; L02.html line 37 (Uses meta) and line 164 (KKT paragraph)", P,
    "Round-5 FAIL E4a-r5-hub-kkt-unused is fixed: L02 line 37 now links kkt-conditions and line 164 states the KKT conditions of max U subject to q.x - w <= 0, x >= 0. Re-derived: pi_s/x_s = mu q_s, mu >= 0, mu(q.x - w) = 0 with x* gives mu = 1/w (pi_s/x*_s = q_s/w), and x*_s > 0 makes the nonnegativity multipliers zero. kkt-conditions is owned by M7 (in closure).")
row("E4a-r6-hub-prereq-usage", "2.9-prose / 2.9-DAG (hub line 63 usage claims)", "index.html line 63 against L01-L09 text", P,
    "Each concept the hub says E4 uses is used: utility maximization and competitive equilibrium (L02 Def 2.2), Pareto efficiency and externality (L03 Def 3.2 and canon-breaks), expected utility (L02 A4), certainty equivalent and Arrow-Pratt (L08), adverse selection (L09), Lagrange multiplier and KKT (L02 line 37 and 164), random variable, expectation, variance, correlation, normal distribution, conditional expectation (L05-L08), linear map and vector space (L01, L04), derivative (L02 R2), gradient (L03 Def 3.3). Orthogonal projection is not linked in any lesson page; L06 uses the projection of v on p (Lemma 6.4, outside this slice). Accepted as use without a link, see the observation in notes.")
row("E4a-r6-hub-numbers", "2.2-numbers", "index.html lines 7, 31, 33, 40-43, 68, 71-73, 113-120, 139", P,
    "100 hours, 72 and 28 hours, 28 percent, 80 percent mastery, seven of eight and 87.5 percent re-derived; all match curriculum.json and the lessons.")
row("E4a-r6-hub-objectives", "2.9-prose", "index.html lines 50-57", P,
    "Each objective names a lesson (1 to 3 in this slice) whose content it describes: L01 decomposition and A2 valuation, L02 two-agent logarithmic equilibrium with budget and market checks, L03 first welfare theorem and MRS check.")
row("E4a-r6-hub-card-claims-L01-03", "2.9-prose", "index.html lines 141-143", P,
    "Card claims for L01 (payoff vectors, decomposition, linear valuation under A2), L02 (budgets, Walras law from binding budgets, closed form with logarithmic utility, two-agent example checked exactly), L03 (feasible allocations, Pareto improvements, MRS between states, proof of no Pareto improvement, equality of rates with price ratios at interior bundles) each appear in the lesson text.")
row("E4a-r6-data-none", "2.8-data", "index.html line 38 and lines 165-168; L01-L03 lab sections", P,
    "No data-files attribute on the hub or L01-L03; labs state 'Inputs are illustrative numbers, not data' and compute exact Fractions. No dataset is named. SIMULATED is not required because no seeded draw appears (grep for random: only the phrase 'No random draws are used').")
row("E4a-r6-references-none", "2.1-citations", "L01-L03 section 9 or 10; index", P,
    "Each lesson states it cites no registry source; data-references lists are empty; no author, year or bibliographic claim appears in the slice (grep for years and surnames). Grossman-Stiglitz, Muth and Milgrom are not cited here.")

# DAG, notation, prose
row("E4a-r6-dag-closure", "2.9-DAG", "index.html, L01-L03 concept links", P,
    "Every data-concept used in the slice is owned by a module in the closure {E1,E2,E3,M1,M2,M3,M4,M7,P0.1} per curriculum.json concepts (for example kkt-conditions M7, externality E1, certainty-equivalent E3, orthogonal-projection M3). Links to concepts.html exist: each anchor id grep-confirmed in course/concepts.html.")
row("E4a-r6-dag-defs-unique", "2.9-DAG", "L01.html line 74, L02.html line 89, L03.html line 78", P,
    "Each of arrow-debreu-security, arrow-debreu-equilibrium and first-welfare-theorem is defined once with dfn data-concept in its assigned lesson; no duplicate dfn for these ids (grep of dfn tags). Internal links L01.html#def-arrow-debreu-security (L02 line 37, L03 line 37) and L02.html#def-arrow-debreu-equilibrium (L03 line 37) point at existing anchors.")
row("E4a-r6-dag-D-terms", "2.9-DAG (plan section 4 D1-D10)", "index.html, L01-L03", P,
    "grep over the slice for 'state price', Bayesian, martingale, common knowledge, Banach, intermediate value, informationally efficient, CARA, noise-trader risk, law of one price, stochastic discount: no hit on the lesson pages; the hub uses the course title 'Stochastic Discount Factor' only in the AP1 unlock line.")
row("E4a-r6-notation-macros", "2.4-notation", "index.html, L01-L03 math", P,
    "notation_scan.py: macros used are \\R, \\E, \\iota, \\Omega, \\bar and standard KaTeX commands; no \\mathbb in any slice page (raw html grep 0 for mathbb). \\R used for the reals in L01 line 79, L02 line 55, L03 line 59. " + S + "notation_scan.out.")
row("E4a-r6-notation-registered-symbols", "2.4-notation", "index.html, L01-L03", P,
    "Registered symbols T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f and Q (notation/notation.json symbols) do not appear in the slice math; the grade letter T is a grade label, not the symbol.")
row("E4a-r6-notation-e-collision", "2.4-notation / define-before-use", "L02.html line 55; L03.html lines 55, 105", P,
    "The security e_s appears in L03 only at line 105 (proof of (b) of Proposition 3.4, where it is named as the Arrow-Debreu security of Definition 1.3) and at line 55 (the sentence that says so). L02 has no e_s (grep: every e_s hit is inside \\bar e_s or e^i_s). L02 line 55 and L03 line 55 statements verified by grep.")
row("E4a-r6-notation-mu-local", "2.4-notation (local symbols)", "L02.html line 164", P,
    "mu first appears in the KKT paragraph as the multiplier; the same sentence names it 'the multiplier mu = 1/w'. Allowed local symbol; not used elsewhere in the slice. Observation only: the definition follows its first appearance inside the same paragraph.")
row("E4a-r6-banned-phrases", "2.9-prose", "index.html, L01-L03", P,
    "check_pages.py BANNED scan passes for E4 pages; the only ellipses are inside Python code blocks (allowed).")
row("E4a-r6-process-words", "2.9-prose", "index.html, L01-L03, lab twins", P,
    "grep for builder, verifier, round, request, unit report, TODO, TBD: no hits in learner text.")
row("E4a-r6-scope-words", "2.9-prose (rule 4)", "index.html, L01-L03 (every, all, always, only, any, same, exactly, in general, never)", P,
    "Each scope claim checked: L01 line 62 (every result that sums over states uses A1; checked against Props 1.4, 1.7, 1.8, 1.10); L02 line 55 (e with superscript always an endowment; grep shows e^i only as endowment); L02 line 94 ('no proposition proves A5'; checked); L03 line 55 (e_s appears only in proof of (b); grep); L03 line 269 (good traded in every state, as Definition 2.3); the E2 and E3 printed-count claims verified against the lab output; 'in general' used only to say existence is not proved.")
row("E4a-r6-define-before-use", "2.9-prose / defined terms", "L01 Def 1.9 before Prop 1.10; L02 Def 2.1 before Def 2.2; L02 line 51; L03 line 51 dfn interior", P,
    "Terms checked: claim, Arrow-Debreu security, security price vector (Def 1.6 before Prop 1.7), expected payoff (Def 1.9 before Prop 1.10), budget set and wealth (Def 2.1 before Def 2.2), demand, Arrow-Debreu equilibrium (Def 2.3), endowment and aggregate endowment, interior (dfn in L03 line 51), feasible allocation (Def 3.1), Pareto improvement (Def 3.2), MRS (Def 3.3). L02 line 51 uses 'excess demand' with an explicit forward cite to Definition 2.3, which defines it.")
row("E4a-r6-hub-forward-naming", "2.9-prose (overview naming)", "index.html lines 33, 53, 56, 139, 149", P,
    "Observation, not a defect: the hub lede and lesson list name noise traders, Arrow-Debreu securities, payoff matrix, informed fraction and posteriors before the lessons that define them. The hub is an overview; the round-4 and round-5 judgment is kept.")
row("E4a-r6-attribution", "2.1-citations / attribution", "index.html, L01-L03", P,
    "No attribution, locator, equation number or date to an outside source appears in the slice; 'Walras' law' names a result (dfn) without citing a source.")

# rounding and numbers
row("E4a-r6-num-L01-M1-rounding", "2.2-numbers", "L01.html line 322 (M1 solution)", P,
    "55/3 = 18.33... stated as 'about 18.33 cents to two decimal places': rounding rule stated. Expected payoff 12.5 and difference 35/6 re-derived.")
row("E4a-r6-num-L01-E3-rounding", "2.2-numbers (plan 2.1 item 1 rounding rule)", "L01.html line 386 (E3 solution)", F,
    "The line reads 'The value at the prices is 340/3 approx 113.33 cents'. 113.33 is a rounded display of 340/3 = 113.333... and the page states no rounding rule for it (the M1 solution on line 322 does state 'to two decimal places'). Plan 2.1 item 1 requires a page that shows a rounded figure to state its rounding rule. 58.75 = 235/4 is exact.",
    "On L01.html line 386 replace 'approx 113.33 cents' with 'approx 113.33 cents, rounded to two decimal places from 340/3' (or write 340/3 cents only).")
row("E4a-r6-num-L01-remaining", "2.2-numbers", "L01.html lines 113-161, 262-281, 320-336, 386, 402-404, 447-449, 463, 484-486", P,
    "Re-derived with rederive_E4a_r6.py (" + S + "rederive_E4a_r6.out): 340/3, 56, 596/3, 235/4, 9/8 (Lab 1 hypothesis and output); 55/3, 12.5, 35/6 (M1); -1/8, 11/8, 17/8 (M3); 1/4 and 1 (R2); quiz values 4.25, 3 and 0.6. All match the page.")
row("E4a-r6-num-L02-example", "2.2-numbers", "L02.html lines 124-126, 187-190, 299-363, 377-393, 429-443, 506-529", P,
    "theta = 9/16 and 7/16; q* = (1/8, 1/32, 1/16); x1 = (9/4, 9/2, 9/4); x2 = (7/4, 7/2, 7/4); q.ebar = 1; residuals 0; ratios 16/9 and 16/7 equal 1/w; M1-M3 values; quiz 0.125 and 0.0625 re-derived (" + S + "rederive_E4a_r6.out).")
row("E4a-r6-num-L02-remark26", "2.2-numbers", "L02.html line 125", P,
    "At q = (2,1,1): wealths 11 and 9; demands (11/4 x3) and (9/4 x3); excess demand (1,-3,1) with unweighted sum -1 and q.z = 0. All re-derived.")
row("E4a-r6-num-L02-misconceptions", "2.2-numbers", "L02.html lines 358, 362, 366", P,
    "State 2 price 1/32 vs state 3 price 1/16 (e-bar 8 vs 4); v = (1,-1,0) has q.v = 3/32; endowment e1 costs 9/16 = w1. All re-derived.")
row("E4a-r6-num-L03-example36", "2.2-numbers", "L03.html lines 119, 250-254, 303-304 (E1), 476 (quiz)", P,
    "MRS agent 1 and agent 2: 12 -> 4, 13 -> 2, 23 -> 1/2; price ratios 4, 2, 1/2. Re-derived in rederive_E4a_r6.out.")
row("E4a-r6-num-L03-R2", "2.4-mathematics / 2.2-numbers", "L03.html lines 385, 360", P,
    "Endowment MRS 12 is 8/3 (agent 1) and 8 (agent 2); derivatives 1/12 and 1/4 of U1 and U2 along the trade; the witness (2,4,3), (2,4,1) is feasible and gives both agents more utility (floats: 0.9679 > 0.8959, 0.6931 > 0.6213). Re-derived.")
row("E4a-r6-num-L03-grid", "2.5-labs / 2.2-numbers", "L03.html lines 124, 259-260, 261", P,
    "Independent grid enumeration (" + S + "rederive_E4a_r6.py): 125 allocations, 0 improvements at the equilibrium, 2 at the endowment, first improvement agent 1 (2,4,3) and agent 2 (2,4,1). Equilibrium fractions 9/16 are off the grid.")

# math
row("E4a-r6-math-L01-props", "2.4-mathematics", "L01.html lines 77-151", P,
    "Prop 1.4 (decomposition), Prop 1.7 (value formula, induction from A2, A1 finiteness), Prop 1.8 (uniqueness of prices), Prop 1.10 (value equals expectation iff q = pi): each proof re-derived; hypotheses A1 and A2 listed before each statement.")
row("E4a-r6-math-L01-A2-sentence", "2.4-mathematics / 2.9-prose", "L01.html line 104", P,
    "A2 excludes quantity discounts, bid-ask spreads and price impact because each makes V nonlinear: a discount breaks V(2x) = 2V(x); a bid-ask spread with a < b values a long position at one price and a short at another, so V(x) + V(-x) is nonzero; price impact makes V depend on size. Checked by reasoning; labelled as an assumption, not derived.")
row("E4a-r6-math-L01-remark111", "2.4-mathematics (grade)", "L01.html line 155", P,
    "Nothing in A1 or A2 forces q = pi: any positive q defines a linear V by Proposition 1.7, so (b) of Proposition 1.10 is not implied. The Part D line 'equal_to_expected_payoff False' is the printed evidence.")
row("E4a-r6-math-L01-R1-countable", "2.4-mathematics / rule 6", "L01.html lines 287, 394-399", P,
    "The coordinate-wise decomposition holds for countable states (only one term nonzero in each state); the step that fails is A2 applied to an infinite sum (A2 stated for two terms). The continuity example is offered as an example, and the page states it does not verify a sufficient condition. Consistent with canon-breaks line 287.")
row("E4a-r6-math-L01-R2-R3-P", "2.4-mathematics", "L01.html lines 345-411", P,
    "P1 (iota = sum of e_s, value sum of q_s), P2 (V(0)=0, V(-x)=-V(x) from A2), P3 (q != pi gives V(e1) = 1/4 != 1/3 = E e1, contrapositive of Prop 1.10), R2 (V = (sum q x)^2 gives 1/4 and 1; linearity fails), R3 (nonnegative value iff q >= 0): all re-derived.")
row("E4a-r6-math-L02-lemma-prop25", "2.4-mathematics", "L02.html lines 99-121", P,
    "Lemma 2.4 uses y = (w/(2 q.iota)) iota, q.y = w/2; Prop 2.5 (Walras law) uses budget perturbation x + delta iota and A1 for strict increase, then sums the two budgets. Hypotheses A1, A3, A4 stated. Re-derived.")
row("E4a-r6-math-L02-cor27-prop28", "2.4-mathematics", "L02.html lines 128-161", P,
    "Cor 2.7 (last market clears) from q.z = 0 and q_s > 0. Prop 2.8 (log demand x_s = pi_s w/q_s) by tangent-line inequality for ln: equality in every tangent forces x = x* using pi_s > 0 (A1); q.x* = w uses sum pi = 1 (A1). Proof complete.")
row("E4a-r6-math-L02-KKT-paragraph", "2.4-mathematics / 2.9-prose", "L02.html line 164", P,
    "Stationarity pi_s/x_s = mu q_s, dual feasibility mu >= 0 and complementary slackness mu(q.x - w) = 0 hold with mu = 1/w at x*; nonnegativity multipliers vanish because x*_s > 0. Primal feasibility (budget q.x* = w, x* >= 0) is stated in the sentence and in the problem, so the list is complete in substance. Lab 2 Part D prints the ratio equal to 1/w (16/9, 16/7).")
row("E4a-r6-math-L02-prop29-remark210", "2.4-mathematics", "L02.html lines 168-185", P,
    "Prop 2.9: theta_1+theta_2 = 1, q*.ebar = 1, x_s = theta_i ebar_s is a demand (Prop 2.8) and clears markets; wealth w_i = theta_i. Remark 2.10: scaling (q,w) by psi leaves x unchanged; q* is not shown unique. Proof re-derived line by line.")
row("E4a-r6-math-L02-R1-R3-P-M", "2.4-mathematics", "L02.html lines 404-470", P,
    "P1 (Corollary 2.7 with s = 3), P2 (scaling psi), P3 (x/ebar = theta_i), R1 (I agents, same proof), R2 (d x_s/d q_s = -x_s/q_s, elasticity -1), R3 (A3 used where: dividing by ebar_s and q*_s, w_i > 0), M1-M3: re-derived and consistent with the proofs.")
row("E4a-r6-math-L03-def33", "2.4-mathematics / rule 6", "L03.html lines 67-74", P,
    "MRS formula pi_s u'(x_s)/(pi_t u'(x_t)) follows from the partial derivatives of U; u' >= 0 from strict increase, nonincreasing from concavity; u' > 0 argued in proof of (b). Definition uses only strictly positive bundles, stated.")
row("E4a-r6-math-L03-prop34a", "2.4-mathematics", "L03.html lines 91-101", P,
    "Proof of (a): Step 1 (strict improvement implies q.y > w), Step 2 (weak improvement implies q.y >= w, using positivity of y and A1, A4 for strict increase), Step 3 (add budgets; contradiction with feasibility). Each step re-read and valid; hypotheses A1, A3, A4 cited.")
row("E4a-r6-math-L03-prop34b", "2.4-mathematics", "L03.html lines 103-110", P,
    "Perturbation d = e_s/q*_s - e_t/q*_t has q*.d = 0; derivative of U at 0 is G = pi_s u'(x_s)/q*_s - pi_t u'(x_t)/q*_t; G = 0 by the sign argument; dividing by pi_t u'(x_t)/q*_t > 0 gives MRS = q*_s/q*_t. Valid.")
row("E4a-r6-math-L03-remark35-P3", "2.9-prose / rule 6 (hypotheses)", "L03.html lines 113-115, 339-343", P,
    "Remark 3.5 and P3 list the hypotheses each part uses: (a) uses strict monotonicity, A1 and A3 through Lemma 2.4 and q* > 0 and no derivative; (b) adds differentiability and strict positivity of x*. Consistent with the proofs.")
row("E4a-r6-math-L03-R1-free-disposal", "2.4-mathematics / 2.9-prose", "L03.html lines 375-379", P,
    "The free-disposal argument is valid. The solution names the last step as the one that 'uses the strict positivity of the prices'; that step needs only q* >= 0, and strict positivity also enters through Lemma 2.4 in the proof of (a). The identification is incomplete but not false, so no change is required; noted for the builder.")
row("E4a-r6-math-L03-R3", "2.4-mathematics", "L03.html lines 389-393", P,
    "Boundary argument: a move that lowers a zero entry leaves the orthant and the utility is minus infinity at zero, so the two-sided derivative in (b) does not exist. Lemma 2.4 gives strictly positive equilibrium bundles. Valid.")
row("E4a-r6-math-L03-M-P-E", "2.4-mathematics", "L03.html lines 300-369", P,
    "M1 MRS 2 (1/3 divided by (2/3)/4); M2 demand (3/2, 3) and MRS 2; M3 feasibility; P1 (no allocation makes every agent better off) via Step 1 and budget sum; P2 MRS = pi_s ebar_t/(pi_t ebar_s) = q*_s/q*_t; E1 printed values 4 and price ratio 4; E2 and E3 consistent with the lab output and the grid argument (grade C with basis).")
row("E4a-r6-math-keyresults", "2.3-grades", "L01 section 7, L02 section 8, L03 section 6 tables", P,
    "Grades T for proved propositions and C for the grid enumeration with its basis, consistent with BUILDER_RULES and with the proofs on the page.")
row("E4a-r6-grades-claims", "2.3-grades", "L01-L03 claim spans", P,
    "Propositions graded T have their hypotheses listed; the grid counts are graded C with basis; no empirical claim is made on these pages (no B or A claim requires counter-evidence).")

# labs
row("E4a-r6-lab-L01-hypothesis", "2.5-labs", "L01.html line 160 vs lab output lines 262-280", P,
    "Hypothesis values 340/3 and 56 cents, linearity with weights 2 and -1/2, 235/4 expected payoff not equal to value, rejections for negative entry and entries summing to 9/8 all match the printed output and the independent re-derivation.")
row("E4a-r6-lab-L01-interpretation", "2.5-labs", "L01.html line 281 (interpretation)", P,
    "Part A exact decomposition; Part B values; Part C equality for one combination ('It checks A2 on that combination only'); Part D False flag; Part E messages. Each sentence matches the output lines.")
row("E4a-r6-lab-L01-code", "2.5-labs", "lab-E4-L01-1 code (L01 lines 161-261; twin tests/labs/E4/lab-E4-L01-1.py)", P,
    "Code read in full: exact Fraction arithmetic; check_probabilities raises ValueError with the messages printed; value and expected_payoff docstrings agree with the code; no RNG; main() called at top level.")
row("E4a-r6-lab-L02-hypothesis", "2.5-labs", "L02.html line 194 vs output lines 315-339", P,
    "Hypothesis: aggregate (4,8,4), wealth shares 9/16 and 7/16, prices, demands, zero residuals, ratios 16/9 and 16/7 equal 1/wealth, scaling by 3 leaves demand unchanged with wealth re-valued, zero endowment rejected with ValueError: all match output and the code.")
row("E4a-r6-lab-L02-interpretation", "2.5-labs", "L02.html line 340", P,
    "'The five budget and market-clearing residuals ... are 0 exactly' matches printed lines (2 budget, 3 market clearing). 'These bundles satisfy Definition 2.3' rests on the closed-form demand of Prop 2.8, which the lab uses; the lab does not separately check optimality, and the page does not claim it does.")
row("E4a-r6-lab-L02-code", "2.5-labs", "lab-E4-L02-1 code (L02 lines 195-314; twin)", P,
    "Code read in full: Part E re-values wealth at scaled prices (demand(PROBS, scaled, dot(scaled, e))); Part F raises for endowment entry zero with the printed message; docstring Part descriptions match each part.")
row("E4a-r6-lab-L03-hypothesis", "2.5-labs", "L03.html line 124 vs output lines 250-260", P,
    "125 grid allocations, 5 grid points per state, 0 improvements at equilibrium, at least one at endowment (output 2), TOL 1e-12, no random draws: all match code and output. The lab description 'a finite check' is consistent with C grade.")
row("E4a-r6-lab-L03-interpretation", "2.5-labs", "L03.html line 261", P,
    "States 'Each flag reads True' (Part A, four rows: 4, 2, 1/2 with price ratios) and the 0 and 2 counts; 'grade C with that basis'. Matches the output.")
row("E4a-r6-lab-L03-code", "2.5-labs", "lab-E4-L03-1 code (L03 lines 125-248; twin)", P,
    "Code read in full: exact Fractions in Part A; floating utilities with TOL 1e-12 in Part B; states printed 1-based; grid_allocations enumerates 5^3 = 125 allocations; improves() uses the documented TOL rule.")
row("E4a-r6-lab-page-equals-twin", "2.5-labs", "L01, L02, L03 data-run code vs tests/labs/E4 twins", P,
    "check_twins_embed.py: each page code block equals its twin after rstrip; each pre.expected equals the twin's output of python -I -W error run from /tmp.")
row("E4a-r6-lab-hypothesis-before-output", "2.5-labs (rule 11)", "L01 lines 160 and 262; L02 lines 194 and 315; L03 lines 124 and 250", P,
    "Each p.hypothesis appears before the code block and before pre.expected in the source order.")
row("E4a-r6-lab-stdlib-no-network", "2.5-labs (rule 11)", "tests/labs/E4/lab-E4-L01-1.py, L02-1.py, L03-1.py imports", P,
    "Imports: fractions (L01, L02), fractions, itertools and math (L03). No NumPy, SciPy, socket, urllib or requests. No RNG (the word random occurs only in the phrase 'No random draws are used').")
row("E4a-r6-lab-main-toplevel", "2.5-labs (rule 10)", "twin last lines", P,
    "Each twin ends with an unconditional main() call; grep for __name__ in the three twins: 0 hits.")
row("E4a-r6-lab-runtime", "2.5-labs", "L01-L03 twins under page_smoke", P,
    "page_smoke E4 (pages index, L01-L03) passes; the run did not use --skip-labs, so every Python lab on these pages ran in the Pyodide smoke path. No per-lab timing was recorded by this verifier.")
row("E4a-r6-lab-no-mutants", "2.6 / ruling (lab twins are demonstrations)", "tests/labs/E4 L01-L03", P,
    "Slice a has no grader; lab twins are demonstrations under the architect ruling, so no mutation test applies to them.")

# quizzes
row("E4a-r6-quiz-hub", "2.9-prose / math", "index.html lines 66-135 (8 placement items)", P,
    "Numeric answers 6 and 8 and the MC keys were re-derived; explanations read against the lessons (E2 L03, L04; E1 Def 2.2 for price taking in L02; M7 Lagrange condition; project Proposition 3 gap).")
row("E4a-r6-quiz-L01", "2.9-prose / math", "L01.html lines 437-505 (9 items)", P,
    "Each key re-derived: coefficient 7 (Prop 1.4); value 4.25 (Prop 1.7); 2V(x) (A2); expected payoff 3 (Def 1.9); one cent per state (Def 1.3); A1 for decomposition; value 0.6 (P1); r = q (Prop 1.8); a size discount (R2). Explanations consistent with the lesson.")
row("E4a-r6-quiz-L02", "2.9-prose / math", "L02.html lines 497-569 (9 items)", P,
    "Keys re-derived: demand pi_s w/q_s (Prop 2.8); 2 (M1); q.z = 0 (Prop 2.5); positivity from Lemma 2.4; 0.125 (Prop 2.9); w_i = theta_i; scaling leaves demand unchanged (Remark 2.10); best affordable bundle (Def 2.2); existence not proved, Prop 2.9 is a construction (Remark 2.10, A5).")
row("E4a-r6-quiz-L03", "2.9-prose / math", "L03.html lines 418-486 (9 items)", P,
    "Keys re-derived: Prop 3.4(a); MRS 2 (M1); Pareto improvement definition; differentiability with positive bundle (Remark 3.5); q1/q2 = 2; equal rates at different bundles (Misconception 2); efficiency rules out (Definition 3.2); MRS^1_12 = 4 (Example 3.6); the monotonicity step (Step 2).")

# hub and placement diagnostic extras
row("E4a-r6-hub-lede-and-ladder", "2.9-prose", "index.html lines 33, 153-163", P,
    "Lede describes lessons 1 to 9 in order and the project; ladder rung text matches the project's ladder (rung 1 worked example prints the bracket after its first three halvings, project line 171; rung 2 completion of indifference_gap, project line 181; rung 3 solve_model(noise_sd, info_cost) with the three keys, project line 316).")
row("E4a-r6-observation-noise-e", "2.4-notation (observation)", "L02.html line 55", P,
    "Observation (not a row defect): the letter e appears both as the Arrow-Debreu security e_s (L01) and as an endowment e^i (L02 on); the L02 and L03 sentences separate them. Recorded for the builder.")

verdict = "PASS" if all(r["status"] == P for r in rows) else "FAIL"
counts = {"rows": len(rows), "pass": sum(r["status"] == P for r in rows), "fail": sum(r["status"] == F for r in rows),
          "unverifiable": 0, "mutants_killed": 0, "mutants": 0}
fragment = {
    "unit": "E4",
    "slice": "a",
    "round": 6,
    "verifier": "Haiku independent verifier, E4-a round 6 (did not build E4; no shared context with the builders)",
    "pin": "4bd8cb94a8e171e80c4c34da1b3f32be7cb93f07",
    "base": "7376a5e216c1e6d99becc76b4cd64028f5b55d3f (round-5 pin). Delta in the slice: L01.html line 397 (R1 solution sentence); L02.html line 37 (Uses meta adds kkt-conditions), line 55 (e superscript sentence), new paragraph after line 163 (KKT); L03.html line 55 (e superscript and e_s sentence). index.html unchanged since the round-5 pin. tests/labs/E4/lab-E4-L01..L03 unchanged. All rows re-derived this round; none carried.",
    "checkout": str(root),
    "scratch": "/tmp only for the twin runs (cwd /tmp, python -I -W error by absolute path). Scripts and logs under ledgers/E4/scripts/E4-a-r6/.",
    "verified_at": "2026-11-04T19:32:33+00:00",
    "verdict": verdict,
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Whole slice read line by line this round: index.html (173 lines), L01.html (524 lines), L02.html (all lines), L03.html (all lines), and the three twins. Every hunk of the round-5 to round-6 delta was read and re-derived.",
        "Round-5 FAIL E4a-r5-hub-kkt-unused is fixed by the KKT paragraph in L02 and the kkt-conditions link on L02 line 37; re-verified PASS (E4a-r6-hub-KKT-claim, E4a-r6-math-L02-KKT-paragraph).",
        "Single FAIL: E4a-r6-num-L01-E3-rounding (L01 line 386 shows 340/3 approx 113.33 with no rounding rule; plan 2.1 item 1). The fix is one phrase.",
        "Non-blocking observations: hub overview names noise traders, Arrow-Debreu securities, payoff matrix, informed fraction and posteriors before their lessons define them (E4a-r6-hub-forward-naming); L03 R1 solution's choice of step (E4a-r6-math-L03-R1-free-disposal); orthogonal projection is not linked in L06 although the hub lists it (E4a-r6-hub-prereq-usage).",
        "Mutants: none. Slice a has no grader; the lab twins are demonstrations under the architect ruling."
    ],
    "summary": counts,
}
out = root / "ledgers" / "E4" / "E4-a.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, counts, verdict)
