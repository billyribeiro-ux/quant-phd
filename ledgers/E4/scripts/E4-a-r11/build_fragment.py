"""E4 slice a, round 11: writes ledgers/E4/E4-a.json from the round-10 row ids and this round's evidence.

Every row id of the round-10 fragment is kept. Each carried id is re-verified in this round (the subject files changed
between pins 00a84795 and 11d7077, so no row is carried by byte identity). Evidence cites the script, command or
line range that backs the row; outputs are archived under ledgers/E4/scripts/E4-a-r11/outputs/.
Run from the checkout root: .venv/bin/python ledgers/E4/scripts/E4-a-r11/build_fragment.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PREV = Path("/Users/billyribeiro/.fanout/frags/E-E4-a.round10.json")
OUT = ROOT / "ledgers/E4/E4-a.json"
SCR = "ledgers/E4/scripts/E4-a-r11"
OUTS = f"{SCR}/outputs"

prev = json.loads(PREV.read_text(encoding="utf-8"))
prev_rows = {r["id"]: r for r in prev["rows"]}

GENERIC = (
    "Round 11, pin 11d7077: re-read in full this round. Commands and scripts below were run in this checkout."
)

# Evidence for each carried id (round 11). Keys are the round-10 ids; values are (status, evidence, optional location).
carried: dict[str, tuple[str, str] | tuple[str, str, str]] = {
    "E4a-r6-cmd-check_pages": ("PASS", f"`.venv/bin/python tools/check_pages.py --unit E4` printed 'check_pages E4: PASS' (exit 0). Output in {OUTS}/check_pages.txt."),
    "E4a-r6-cmd-check_dag": ("PASS", "`.venv/bin/python tools/check_dag.py --unit E4` exit 0, 'check_dag E4: PASS' (run this round; the unit DAG check covers index and L01 to L03 links)."),
    "E4a-r6-cmd-run_labs": ("PASS", f"`tools/run_labs.py --unit E4 --page L01|L02|L03`: each 'run_labs E4: PASS (1/1)', exit 0 (archived in {OUTS}/gate_commands.txt)."),
    "E4a-r6-cmd-page_smoke": ("PASS", f"`.venv/bin/python tools/page_smoke.py --unit E4` exit 0; 'page_smoke modules/E/E4/index.html: PASS', 'L01.html: PASS', 'L02.html: PASS', 'L03.html: PASS', 'E4: PASS' (archived {OUTS}/page_smoke.txt). Labs ran in the Pyodide runtime; the in-browser step times are 0.0 s per lab."),
    "E4a-r6-cmd-twins-alone": ("PASS", f"Each twin run alone as `.venv/bin/python -I -W error tests/labs/E4/lab-E4-L0n-1.py` (CPython 3.14.8): rc 0 for L01, L02, L03, stderr empty. Checked by {SCR}/lab_page_twin_check.py (30 PASS, 0 FAIL)."),
    "E4a-r6-cmd-twin-embed": ("PASS", f"{SCR}/lab_page_twin_check.py: page data-run text equals the twin source (only the trailing newline is stripped by the embedder, verified by a separate comparison) and pre.expected equals the twin stdout for L01, L02, L03."),
    "E4a-r6-cmd-ruff": ("PASS", "`.venv/bin/ruff check` on the three twins: 'All checks passed!'; `ruff format --check`: '3 files already formatted' (archived gate_commands.txt)."),
    "E4a-r6-cmd-mypy": ("PASS", "`.venv/bin/mypy --no-incremental` on the three twins: 'Success: no issues found in 3 source files' (archived gate_commands.txt)."),
    "E4a-r6-cmd-pytest": ("PASS", "`.venv/bin/python -m pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py` rc 0, all dots (archived gate_commands.txt)."),
    "E4a-r6-cmd-verify_refs": ("PASS", f"`verify_refs.py --unit E4` is a live run and was not executed (no network use). The unit cites no registry key (no data-cite in index, L01 to L03; data-references lists empty at L01 line 512, L02 line 576, L03 line 494), so the live run has no entry to resolve. `verify_refs.py --offline` over the whole registry: 'offline integrity: 560 entries, 0 problems' (archived {OUTS}/verify_refs.txt)."),
    "E4a-r6-cmd-check_projects": ("PASS", "`tools/check_projects.py --unit E4`: 'check_projects E4: PASS', exit 0 (cross-slice; the project page is slice e's, run for completeness)."),
    "E4a-r6-struct-lesson-order": ("PASS", "L01 to L03 section order read in full: why-it-matters, core sections, inline lab (lab-E4-L0n-1 before canon-breaks), canon-breaks, misconceptions, problem set, key results, quiz, references, lesson-nav (L01 lines 51, 158 to 282, 284, 294, 312, 417, 433, 509; L02 lines 51, 193, 343, 353, 371, 476, 493, 573; L03 lines 51, 122, 264, 276, 294, 399, 415, 491)."),
    "E4a-r6-struct-counts": ("PASS", f"{SCR}/structure_slice_a.py (archived {OUTS}/structure.out): quiz items 9 on each lesson (8 to 15 required); misconceptions 3 on each lesson; each of Mechanics, Proof, Empirical, Research has 3 problems on L01, L02, L03."),
    "E4a-r6-struct-why-words": ("PASS", f"{SCR}/structure_slice_a.py: why-it-matters words L01 108, L02 117, L03 120 (limit 120; {OUTS}/structure.out)."),
    "E4a-r6-struct-solution-words": ("PASS", f"{SCR}/structure_slice_a.py: 12 details.solution blocks per lesson, none under 15 words ({OUTS}/structure.out)."),
    "E4a-r6-hours-arith": ("PASS", "index line 29 data-hours-lessons=72, data-hours-project=28; line 43 eyebrow '72 h lessons · 28 h project (28%)'; line 41 hours-split widths 72% and 28%; L01 to L03 data-hours=8 (L01 line 2, L02 line 2, L03 line 2) and eyebrow '8 study hours'. 9 x 8 = 72; 72 + 28 = 100; 28/100 = 28%, inside 10 to 40 percent."),
    "E4a-r6-hub-placement": ("PASS", "index lines 66 to 135: 8 items (lines 70, 75, 84, 93, 102, 107, 116, 125 = six prerequisite items and two data-skill items); data-mastery 0.8 (line 66). Line 68 arithmetic: 0.8 x 8 = 6.4, so seven correct; 6/8 = 75 percent, 7/8 = 87.5 percent (re-derived)."),
    "E4a-r6-hub-titles": ("PASS", "index cards lines 141 to 149 titles equal the h1 of each lesson: L01 line 35 'Arrow–Debreu securities and state-contingent payoffs'; L02 line 35 'Arrow–Debreu equilibrium'; L03 line 35 'The first welfare theorem'; L04 to L09 h1 (grep this round): 'Complete and Incomplete Markets', 'Rational-Expectations Equilibrium', 'Noisy rational-expectations equilibrium', 'Price informativeness', 'The Grossman–Stiglitz Paradox', 'The No-Trade Theorem'. All nine card titles equal the lesson h1 text exactly."),
    "E4a-r6-hub-unlocks": ("PASS", "index line 36 lists AP1, AP6, MS1, SR1. Read from curriculum/curriculum.json (this round): the modules whose prereqs contain E4 are exactly AP1, AP6, MS1, SR1; titles 'No-Arbitrage & the Stochastic Discount Factor', 'Intermediary & Institutional Asset Pricing', 'Microstructure Theory', 'Runs, Liquidity & Fire Sales' match."),
    "E4a-r6-hub-prereq-titles": ("PASS", "index line 35: E2 'Game Theory & Information Economics', E3 'Decision Theory Under Risk & Ambiguity', M7 'Optimization' equal curriculum.json titles (this round)."),
    "E4a-r6-hub-KKT-claim": ("PASS", "index line 63 'From M7 it uses Lagrange multipliers and the KKT conditions'; L02 line 164 uses the KKT conditions (paragraph with 'The maximizer also satisfies the KKT conditions')."),
    "E4a-r6-hub-prereq-usage": ("PASS", "FIXED since round 10. index line 63 now lists M3 as 'linear maps and vector spaces' only. `grep -c orthogonal index.html L01.html L02.html L03.html` finds no concept link to orthogonal-projection in index; each remaining hub concept link is used by a lesson (grep for data-concept this round: utility-maximization in L02; competitive-equilibrium in L02, L06, L08; pareto-efficiency in L03, L09; externality in L03; expected-utility in L02, L06, L08; certainty-equivalent and arrow-pratt-risk-aversion in L08; adverse-selection in L09; lagrange-multiplier and kkt-conditions in L02; random-variable, expectation, variance, correlation, normal-distribution, conditional-expectation-elementary in L05 to L09 or L01; linear-map and vector-space in L01 and L04; derivative in L02, L08; gradient in L03)."),
    "E4a-r6-hub-numbers": ("PASS", "index numbers re-derived this round: 72 and 28 (line 29, 41, 43), 28% (line 43), 8 objectives (lines 50 to 57), 80 percent and 7 of 8 (line 68), 75 and 87.5 percent (line 68), 8 items (line 66 to 135), 9 lessons (line 139), 1/2 and 1/4 in the placement items (lines 71, 103)."),
    "E4a-r6-hub-objectives": ("PASS", "index lines 50 to 57: eight objectives with measurable verbs (Decompose, Solve, Prove, Decide, Solve, Derive, Compute, Write), within 4 to 8."),
    "E4a-r6-hub-card-claims-L01-03": ("PASS", "index lines 141 to 143 card claims checked against L01 (Props 1.4, 1.7; Assumption A2; Definition 1.3), L02 (Walras' law, closed-form logarithmic equilibrium with a two-agent example checked exactly, Lab 2) and L03 (Pareto improvement, MRS, interior equilibria, Lab 3). Each claim has its text in the lesson."),
    "E4a-r6-data-none": ("PASS", "index line 38 and line 167 say no real dataset. Twins L01 to L03 do not open a file (grep for open(, requests, urllib, socket: no match in tests/labs/E4/lab-E4-L0[123]-1.py). Lab sections carry no data-files attribute (L01 to L03 section tags at L01 line 158, L02 line 192, L03 line 122)."),
    "E4a-r6-references-none": ("PASS", "index and L01 to L03 contain no data-cite and no data-locator (grep, this round). data-references lists are empty (L01 line 512, L02 line 576, L03 line 494). Section 9 (L01), 10 (L02), 8 (L03) say the lesson cites no registry source."),
    "E4a-r6-dag-closure": ("PASS", f"{SCR}/structure_slice_a.py: all 38 concept links (prerequisite anchors to ../../../concepts.html#id and lesson anchors) resolve to ids present in course/concepts.html or to a def in an earlier lesson; no lesson links a later one (archived {OUTS}/structure.out)."),
    "E4a-r6-dag-defs-unique": ("PASS", "dfn owners from structure_slice_a.py: arrow-debreu-security (L01 line 74), arrow-debreu-equilibrium (L02 line 89), first-welfare-theorem (L03 line 78); each defined once; dfn id equals def-<data-concept>."),
    "E4a-r6-dag-D-terms": ("PASS", "grep (case-insensitive) of index, L01 to L03 for the plan's D1 to D10 names: 'state price' 0 hits; 'martingale', 'Bayes', 'Banach', 'intermediate value', 'two-fund', 'determinacy', 'efficient markets', 'Kyle', 'common knowledge' 0 hits (common knowledge is not used); 'Stochastic Discount' only in the AP1 title at index line 36. 'Walras' appears as a plain dfn (L02 line 110) and as the plain term 'Walras' law', which the plan allows (D9)."),
    "E4a-r6-notation-macros": ("PASS", "math segments of index, L01 to L03 (structure scan): the only macros are \\E, \\Prob, \\R (all registered in notation/notation.json: \\E expectation operator, \\Prob probability measure, \\R real numbers). No raw \\mathbb{E}."),
    "E4a-r6-notation-registered-symbols": ("PASS", "math segments scanned for \\mathbb (none), \\Phi (none), \\gamma (none), \\ast (none), \\mathbb{Q} (none), bare T as a symbol (none). Registered symbols T, Phi, gamma_3, gamma_4, R^ast, R^{e ast}, R_f, Q are not used (notation/notation.json 'symbols')."),
    "E4a-r6-notation-e-collision": ("PASS", "L02 line 55 explains that e^i is the endowment and that the Arrow–Debreu security e_s of L01 carries only a state subscript; L03 line 55 repeats this. The registered symbols have no e."),
    "E4a-r6-notation-mu-local": ("PASS", "mu is not a registered symbol (notation.json has no mu entry). L02 line 164 uses mu as the KKT multiplier. The plan lists mu as a local symbol for a mean, which the lesson does not use; no registered meaning is overwritten. Observation only, see notes."),
    "E4a-r7-notation-u-local": ("PASS", "u is not registered. L02 lines 68 to 71 use u_i for utilities and L03 line 69 uses u_i'; the plan reserves u for noise supply in L06. Local, defined on first use in each lesson. Observation only, see notes."),
    "E4a-r6-banned-phrases": ("PASS", f"{SCR}/structure_slice_a.py: banned strings TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly absent from visible text of index, L01, L02, L03 (archived {OUTS}/structure.out). The three-dot sequence appears only inside Python code (`tuple[Fraction, ...]`) and the TeX \\ldots in math."),
    "E4a-r6-process-words": ("PASS", "structure_slice_a.py process-word scan (builder, verifier, planner, fixer, architect, REQUESTS, unit report): no hits. The whole-word scan for 'round' finds no hit; the prose uses 'rounded' (L01 line 386) and 'rounding' (L01 line 511), which are ordinary words."),
    "E4a-r6-scope-words": ("PASS", "every, all, always, only, any, same, exactly, never in index, L01 to L03 read in full this round. Each universal claim has a proof (L01 Prop 1.4, 1.7, 1.10; L02 Lemma 2.4, Prop 2.5, Cor 2.7, Prop 2.8, Prop 2.9; L03 Prop 3.4), a finite check named as grade C (L03 Lab 3 Part B, E3 solution), or an explicit hypothesis (A1 to A5)."),
    "E4a-r6-define-before-use": ("PASS", "L01: Definition 1.1 (state space) before Assumption A1, Def 1.2 (claim), Def 1.3 (security) before Prop 1.4, A2 (line 99) before Def 1.6 (line 108), Def 1.9 (line 137) before Prop 1.10. L02: Def 2.1 (line 74) before Def 2.2 (line 83), Def 2.3 (line 88), Lemma 2.4 (line 100) before Prop 2.5 (line 110). L03: Def 3.1 to 3.3 (lines 58, 63, 68) before Prop 3.4 (line 81); 'interior' is defined in L03 line 51 before its uses."),
    "E4a-r6-hub-forward-naming": ("PASS", "index lines 33, 53, 56, 139, 149 use later-lesson terms (informed fraction, noise traders, posteriors) in overview text, which is not a lesson. Each term is defined in its lesson: L06 has plain dfn elements for 'noise trader', 'informed fraction' and 'posterior' (grep this round); L08 defines 'equilibrium informed fraction'. Observation only, see notes."),
    "E4a-r6-attribution": ("PASS", "index and L01 to L03 contain no bibliographic record, locator or theorem attribution outside Assumption and Proposition titles. The name 'Grossman–Stiglitz paradox' is the curriculum's lesson title (curriculum.json concept grossman-stiglitz-paradox), not a registry citation, and no key or year is typed for it in these pages."),
    "E4a-r6-num-L01-M1-rounding": ("PASS", "L01 line 322 (M1 solution): 55/3 = 18.333..., printed as 'about 18.33 cents to two decimal places'; 35/6 difference; 25/2 = 12.5 expected payoff. Re-derived in rederive_slice_a.py ('L01 M1 value 55/3', 'L01 M1 expected payoff 25/2', 'L01 M1 difference 35/6': PASS)."),
    "E4a-r6-num-L01-E3-rounding": ("PASS", "L01 line 386 (E3 solution): 235/4 = 58.75; 340/3 = 113.33 rounded from 340/3; both re-derived (rederive_slice_a.py PASS lines for 340/3 and 235/4)."),
    "E4a-r6-num-L01-remaining": ("PASS", "L01 numbers at lines 113 to 161, 262 to 281, 320 to 336, 386, 402 to 404, 447 to 449, 463, 486 re-derived: 340/3, 56, 596/3, 235/4, 4.25, 3, 0.6, V(2x) = 2V(x), 1/4 vs 1/3 (rederive_slice_a.py PASS)."),
    "E4a-r6-num-L02-example": ("PASS", "L02 Example 2.11 (line 189): theta = 9/16, 7/16; q* = (1/8, 1/32, 1/16); bundles (9/4, 9/2, 9/4), (7/4, 7/2, 7/4). Re-derived: rederive_slice_a.py 'L02 Example 2.11 theta shares', 'L02 Prop 2.9 prices', 'L02 Example 2.11 bundles' PASS."),
    "E4a-r6-num-L02-remark26": ("PASS", "L02 Remark 2.6 (line 125): wealths 11 and 9 at q = (2,1,1); demands (11/4 x3) and (9/4 x3); excess demand (1,-3,1); unweighted sum -1; q.z = 0. Re-derived (rederive_slice_a.py 'L02 Remark 2.6' PASS x3)."),
    "E4a-r6-num-L02-misconceptions": ("PASS", "L02 misconception 1 (line 358): q*_2 = 1/32, q*_3 = 1/16, ebar_2 = 8, ebar_3 = 4. Misconception 2 (line 362): v = (1,-1,0), q*.v = 3/32 (re-derived PASS). Misconception 3 (line 366): e^1 costs 9/16 = w_1 (re-derived PASS)."),
    "E4a-r6-num-L03-example36": ("PASS", "L03 Example 3.6 (line 119): MRS agent 1 = 4, 2, 1/2 and agent 2 the same; price ratios 4, 2, 1/2; re-derived (rederive_slice_a.py 'L03 Example 3.6 agent 1 MRS', 'agent 2 MRS', 'price ratios' PASS)."),
    "E4a-r6-num-L03-R2": ("PASS", "L03 R2 solution (line 386): y1 = (3-e, 4+4e, 1), y2 = (1+e, 4-4e, 3); derivatives 1/12 and 1/4 (re-derived PASS 'L03 R2 derivatives'); MRS 8/3 and 8 (re-derived PASS 'endowment MRS_12')."),
    "E4a-r6-num-L03-grid": ("PASS", f"L03 grid claims (lines 124, 258 to 261 of the page; 125 allocations, 0 at equilibrium, 2 at endowment) re-derived by {SCR}/rederive_slice_a.py: count at TOL 1e-12, 1e-9, 0 and with 60-digit Decimal logs gives 0 at equilibrium and 2 at endowment (archived {OUTS}/rederive.out)."),
    "E4a-r6-math-L01-props": ("PASS", "L01 lines 77 to 151: Prop 1.4 (decomposition, A1), Prop 1.7 (value formula, A1 and A2), Prop 1.8 (uniqueness, proof takes x = e_s), Prop 1.10 ((a) iff (b), both directions in the proof). Each proof re-read; each follows from the stated assumptions."),
    "E4a-r6-math-L01-A2-sentence": ("PASS", "L01 line 104: A2 excludes quantity discounts, bid-ask spreads and price impact because each makes V nonlinear. Bid-ask (ask and bid differ, so V(-x) differs from -V(x)), quantity discounts (V(2x) differs from 2V(x)) and price impact (cost quadratic in size) are nonlinear; read, no counterexample needed for a scope statement that names the nonlinearity."),
    "E4a-r6-math-L01-remark111": ("PASS", "L01 line 155 (Remark 1.11): Lab 1 Part D (value 340/3 against expected payoff 235/4, flag False) shows the prices differ from the probabilities; Prop 1.10 then gives q != pi (logic re-checked: (a) fails, so (b) fails)."),
    "E4a-r6-math-L01-R1-countable": ("PASS", "L01 lines 287, 394 to 399: R1 solution and canon item 1 agree: the decomposition holds coordinatewise for countable S; the extension of A2 to infinite sums is the step not justified. Consistent with Def 1.1 (finite S) and Assumption A1."),
    "E4a-r6-math-L01-R2-R3-P": ("PASS", "L01 lines 345 to 411: P1 (iota = sum of e_s, V(iota) = sum q_s), P2 (V(0)=0, V(-x) = -V(x) from A2 with a = 0 and a = -1), P3 (V(e_1) = 1/4 vs E e_1 = 1/3), R2 (V(2e_1) = 1 vs 2V(e_1) = 1/2), R3 (nonnegativity iff q >= 0). Each re-derived; PASS."),
    "E4a-r6-math-L02-lemma-prop25": ("PASS", "L02 lines 99 to 121: Lemma 2.4 (y = (w/(2 q.iota)) iota, U(y) finite, zero entry gives -infinity); Prop 2.5 (budgets bind by strict monotonicity and A1; the sum over agents gives q.(x1+x2-ebar) = 0). Proof steps re-read: valid under A1, A3, A4 as stated."),
    "E4a-r6-math-L02-cor27-prop28": ("PASS", "L02 lines 128 to 161: Cor 2.7 (from Prop 2.5 with q_s > 0); Prop 2.8 proof: tangent-line inequality for ln, the identity pi_s/x*_s = q_s/w turns the sum into (q.x - w)/w <= 0, equality forces x = x*. Re-derived PASS."),
    "E4a-r6-math-L02-KKT-paragraph": ("PASS", "L02 line 164: KKT conditions for max U s.t. q.x - w <= 0 and x >= 0: pi_s/x_s = mu q_s, mu >= 0, mu(q.x - w) = 0, with mu = 1/w; Lab 2 Part D prints 16/9 and 16/7, equal to 1/w (rederive_slice_a.py 'L02 Part D ratios' PASS)."),
    "E4a-r6-math-L02-prop29-remark210": ("PASS", "L02 lines 168 to 185: Prop 2.9 proof (theta_1 + theta_2 = 1, q*.ebar = 1, w_i = theta_i, x*_s = theta_i ebar_s, clearing); Remark 2.10 (scale invariance of demand under (psi q, psi w)). Re-derived PASS (rederive_slice_a.py L02 prices, wealth, clearing)."),
    "E4a-r6-math-L02-R1-R3-P-M": ("PASS", "L02 lines 404 to 470: M1 (x = (1,2), spending 1/2), M2 (x = (3/4, 3/8, 3/2), spending 3), M3 (ebar = (4,4), q* = (1/8,1/8), x = (2,2)), P1 (Cor 2.7 with s = 3), P2 (psi scaling), P3 (x/ebar = theta), R1 (I agents), R2 (-x/q elasticity = -1), R3 (where A3 is used). Each re-derived; PASS."),
    "E4a-r6-math-L03-def33": ("PASS", "L03 lines 67 to 74 (Def 3.3): MRS = (pi_s u'(x_s))/(pi_t u'(x_t)) from U = sum pi u; the 'units given up' reading agrees with the M1 solution (line 304: 'the agent would give up 2 units of the good in state 2 for one more unit in state 1')."),
    "E4a-r6-math-L03-prop34a": ("PASS", "L03 lines 91 to 101 (Prop 3.4 (a) proof, Steps 1 to 3): re-read; Step 1 (strict improvement gives q.y > w), Step 2 (weak improvement gives q.y >= w, using A4 and A1 with delta iota), Step 3 (adding gives q.(y1+y2) > q.ebar, contradiction). Valid under A1, A3, A4."),
    "E4a-r6-math-L03-prop34b": ("PASS", "L03 lines 103 to 110 (Prop 3.4 (b) proof): d = e_s/q_s - e_t/q_t has q.d = 0; G = pi_s u'(x_s)/q_s - pi_t u'(x_t)/q_t = 0 by the two-sided argument; u' > 0 from monotonicity and concavity (the zero-derivative argument on (x_t, infinity) contradicts strict monotonicity). Valid."),
    "E4a-r6-math-L03-remark35-P3": ("PASS", "L03 lines 113 to 115 (Remark 3.5) and lines 339 to 343 (P3): each hypothesis of part (a) and part (b) is named as used in the proof; the claim that (a) survives without differentiability is supported by a proof that uses no derivative."),
    "E4a-r6-math-L03-R1-free-disposal": ("PASS", "L03 lines 375 to 379 (R1 solution): free disposal with q* nonnegative gives q.(ebar - (y1+y2)) >= 0 and the contradiction; positivity enters only through Lemma 2.4 (finite utilities). Re-derived."),
    "E4a-r6-math-L03-R3": ("PASS", "L03 lines 389 to 393 (R3 solution): the (b) argument needs both directions of the perturbation; a zero entry removes one direction, and Lemma 2.4 gives strictly positive equilibrium bundles. Consistent with Remark 3.5."),
    "E4a-r6-math-L03-M-P-E": ("PASS", "L03 lines 300 to 369: M1 (MRS_12 = 2 for pi = (1/3,2/3), x = (1,4)), M2 (x = (3/2, 3), MRS = 2 = q1/q2), M3 (feasible split), P1 (no all-gain allocation), P2 (MRS = pi_s ebar_t/(pi_t ebar_s) = q*_s/q*_t), P3, E1 to E3 (Lab 3 Part A and B readings, 8/3 and 8, 0 and 2 counts). Each re-derived this round."),
    "E4a-r6-math-keyresults": ("PASS", "Key-results tables: L01 section 7 (lines 417 to 431), L02 section 8 (lines 476 to 491), L03 section 6 (lines 399 to 413). Each row's grade and source checked against the proposition or lab part it cites."),
    "E4a-r6-grades-claims": ("PASS", "Grades on claim spans in index, L01 to L03: theorems and propositions T (L01 lines 78, 113, 127, 142; L02 lines 100, 110, 128, 143, 169; L03 lines 81), the grid count C (L03 lines 409, 261 and E3 solution), the lab exact results T (L01 line 427). No B or C claim omits counter-evidence the lesson needs."),
    "E4a-r6-lab-L01-hypothesis": ("PASS", "L01 line 160 hypothesis: coefficients 100, 40, 0, 250 (Lab 1 Part A lines 262 to 268); value 340/3 and 56 (Part B line 270); linearity (Part C line 273); expected payoff 235/4 (Part D line 275); rejections (Part E). Each printed value matches."),
    "E4a-r6-lab-L01-interpretation": ("PASS", "L01 line 281 interpretation: Part A exact decomposition, Part B values 340/3 and 56, Part C linearity for one combination (weights 2 and -1/2), Part D False flag, Part E two messages. It names no printed line that is not printed (see E4a-r11-lab-L01-partE-label for the one label defect in Part E)."),
    "E4a-r6-lab-L01-code": ("PASS", f"lab-E4-L01-1: page code (L01 lines 161 to 261) equals tests/labs/E4/lab-E4-L01-1.py (trailing newline only), checked by {SCR}/lab_page_twin_check.py. The code computes exact Fractions; no random draw."),
    "E4a-r6-lab-L02-hypothesis": ("PASS", "L02 line 194 hypothesis: aggregate (4,8,4), wealth shares 9/16 and 7/16, prices (1/8, 1/32, 1/16), demands (9/4, 9/2, 9/4) and (7/4, 7/2, 7/4), zero residuals, ratios 16/9 and 16/7, scaling by 3 leaves demand unchanged, zero endowment rejected. Each matches Lab 2 output (L02 lines 316 to 339)."),
    "E4a-r6-lab-L02-interpretation": ("PASS", "L02 line 340 interpretation: five budget and clearing residuals and the Walras residual are 0; Part D ratio equals one over wealth; Part E scaling flag depends on re-valuation (checked by the line 'With wealth held fixed, the demand would fall by a factor of 3'); the lab does not show uniqueness, consistent with Remark 2.10."),
    "E4a-r6-lab-L02-code": ("PASS", f"lab-E4-L02-1: page code (L02 lines 195 to 314) equals tests/labs/E4/lab-E4-L02-1.py (trailing newline only), checked by {SCR}/lab_page_twin_check.py."),
    "E4a-r6-lab-L03-hypothesis": ("PASS", "L03 line 124 hypothesis: Part A prints 4, 2, 1/2 for both agents, each flag True; Part B grid of 125 with shares in {0,1/4,1/2,3/4,1}; 0 improvements at equilibrium, at least one at endowment; TOL 1e-12. Matches Lab 3 output (L03 lines 250 to 260) and the twin (GRID, TOL = 1e-12, product over three states = 125)."),
    "E4a-r6-lab-L03-interpretation": ("PASS", "L03 line 261 interpretation: flags True; 0 improvements of 125; 2 improvements of the endowment, first one (2,4,3)/(2,4,1); zero count is grade C. Matches output lines 258 to 260."),
    "E4a-r6-lab-L03-code": ("PASS", f"lab-E4-L03-1: page code (L03 lines 125 to 249) equals tests/labs/E4/lab-E4-L03-1.py (trailing newline only), checked by {SCR}/lab_page_twin_check.py."),
    "E4a-r6-lab-page-equals-twin": ("PASS", f"{SCR}/lab_page_twin_check.py: for L01, L02, L03 the data-run text equals the twin (trailing newline only) and pre.expected equals the stdout of `python -I -W error` (30 PASS)."),
    "E4a-r6-lab-hypothesis-before-output": ("PASS", "Hypothesis paragraphs at L01 line 160, L02 line 194, L03 line 124 precede the code and expected blocks (checked by the script: 'hypothesis paragraph precedes the code block' PASS for three labs)."),
    "E4a-r6-lab-stdlib-no-network": ("PASS", "Imports in the three twins: fractions, math, itertools (L03), __future__; no numpy, no network, no file read (grep this round)."),
    "E4a-r6-lab-main-toplevel": ("PASS", "Each of the three twins ends with an unconditional `main()` call (L01 line 261 of the page, L02 line 314, L03 line 249) and has no `if __name__ == \"__main__\"` guard (grep)."),
    "E4a-r6-lab-runtime": ("PASS", "page_smoke Pyodide timings for lab-E4-L01-1, L02-1, L03-1: 0.0 s each (archived page_smoke.txt), under 10 s."),
    "E4a-r6-lab-no-mutants": ("PASS", "Lab twins are demonstrations; mutation testing applies to the project grader only (plan ruling). Slice a has no grader."),
    "E4a-r6-quiz-hub": ("PASS", "Placement quiz index lines 66 to 135: each of the 8 items has an explain block and a correct answer as stated (numeric 6, 8; MC correct options at lines 78, 87, 96, 110, 119, 128)."),
    "E4a-r6-quiz-L01": ("PASS", "L01 quiz lines 437 to 506 (9 items): every correct option and numeric answer re-derived (5 in state 2; 4.25; V(2x) = 2V(x); 3; Def 1.3; Prop 1.4 with A1; 0.6 within 0.0005; r = q; the size discount). Explanations read against the lesson."),
    "E4a-r6-quiz-L02": ("PASS", "L02 quiz lines 497 to 570 (9 items): answers re-derived (pi_s w/q_s; 2; q.z = 0; Lemma 2.4 reason; 0.125; theta_i; invariance; the demand definition; the qualitative claim about Proposition 2.9). Item 9 explanation has a wrong section reference: see E4a-r11-delta-L02-L568."),
    "E4a-r6-quiz-L03": ("PASS", "L03 quiz lines 418 to 487 (9 items): answers re-derived (part (a) statement; 2; equal-rate reading; hypotheses of (b); 2; 'Yes' with Example 3.6; efficiency reading; 4; monotonicity reason)."),
    "E4a-r6-hub-lede-and-ladder": ("PASS", "index lede line 33 and ladder lines 155 to 161: rung 1 and rung 2 descriptions match project.html (lab-E4-project-1 prints brackets after halvings 1 to 3; rung 2 blank is the return of indifference_gap)."),
    "E4a-r6-observation-noise-e": ("PASS", "L02 line 55 explains the e^i notation; no conflict with the registry."),
    "E4a-r7-math-L03-R2-compensation": ("PASS", "L03 line 386 (R2 solution, last sentences): agent 1 gives 1 unit of state 1 and gets 4 units of state 2; its rate 8/3 is compensation, so it gains; agent 2 has rate 8. Consistent with Definition 3.3 (units of state t given up for one more unit in state s)."),
    "E4a-r7-data-simulated-labels": ("PASS", "No SIMULATED label is needed in L01 to L03 (no seeded draw). Labels on the other slices' labs confirmed this round: lab-E4-L06-1 line 177 ('Part E: SIMULATED sample check'), lab-E4-L07-1 line 163 ('Part F: SIMULATED sample check'), lab-E4-L08-1 docstring line 5 and Part A output 'part A (SIMULATED draws)'."),
    "E4a-r7-hub-cross-unit-titles": ("PASS", "index line 63 and curriculum titles: E2 L03 h1 'Adverse Selection' (E2 L03.html line 35) and E2 L04 h1 'Signaling' (E2 L04.html line 36) match the placement items' references; E3 index h1 'Decision Theory Under Risk &amp; Ambiguity' (E3 index.html line 32) matches the hub prerequisite name."),
    "E4a-r7-delta-coverage": ("PASS", "git diff 00a84795..11d7077 restricted to slice-a paths: index.html (12 lines), L01.html (4), L02.html (4), L03.html (2); lab twins L01 to L03 unchanged. Every hunk read this round (see E4a-r11-delta-* rows). Diff recorded from git diff --stat."),
    "E4a-r7-rederive-all-numbers": ("PASS", f"Every number in index, L01 to L03 prose re-derived by {SCR}/rederive_slice_a.py (51 PASS lines; three FAIL lines printed on the first run were errors in the verifier's own test expressions (an R2 expression, an M2 MRS call on the wrong probability vector, and a tuple comparison), corrected and re-run; archived {OUTS}/rederive.out)."),
    "E4a-r8-delta-index-lede": ("PASS", "index line 33 (lede) read this round: sentences name Lessons 1 to 9 correctly and the project's solver and report."),
    "E4a-r8-delta-index-data": ("PASS", "index lines 38 and 167 (data claims, changed in 11d7077) checked against the twins: L06 Parts A to D exact (lab-E4-L06-1 'Parts A to D are exact' docstring line 211; output shows exact Fractions), L07 Parts A to E exact (output 'Part A ... 1/3'), L08 Parts B to D double precision and Part A seeded (lab-E4-L08-1 docstring line 5), L03 Part B floats (twin line 139 onward), L09 exact (Fraction import)."),
    "E4a-r8-delta-L01-R1": ("PASS", "L01 lines 395 to 397 (R1 problem and solution) read this round; consistent with canon item 1 (line 287)."),
    "E4a-r8-delta-L01-references": ("PASS", "L01 line 511 (references paragraph): 'cites no registry source'; the figures it names (340/3, 56, 596/3, 235/4) are the Lab 1 Parts B to D outputs (output lines 270, 273, 275, 276)."),
    "E4a-r8-delta-L02-line55": ("PASS", "L02 line 55 read this round (see E4a-r6-notation-e-collision)."),
    "E4a-r8-delta-L02-canon": ("PASS", "L02 line 349 (canon item 4, changed in 11d7077): 'Full sharing is a property of the logarithmic economy of Proposition 2.9.' The text matches Prop 2.9 (x^{i*}_s = theta_i ebar_s) and the proof's logarithmic demand."),
    "E4a-r8-delta-L03-line55": ("PASS", "L03 line 55 read this round: the security e_s is used only in the proof of Prop 3.4 (b) (line 105), as stated."),
    "E4a-r8-delta-L03-E2": ("PASS", "FIXED since round 10. L03.html line 361 (E2 solution) now reads 'Relative to the endowment, each agent's expected utility rises by (1/4) ln(4/3) > 0 at this witness, which is checked by hand (grade T).' Re-derived this round (rederive_slice_a.py 'L03 E2 witness gain = (1/4) ln(4/3) for both agents' and 'lab witness gain 0.0719205': PASS). The lab witness is (2,4,3),(2,4,1), so the sentence now refers to the witness it describes."),
    "E4a-r8-delta-L03-R1": ("PASS", "L03 line 378 (R1 solution) read this round and re-derived (see E4a-r6-math-L03-R1-free-disposal)."),
    "E4a-r8-delta-L03-R2": ("PASS", "L03 line 385 to 386 (R2 solution) read this round and re-derived (see E4a-r6-num-L03-R2)."),
    "E4a-r8-grid-recount": ("PASS", f"{SCR}/rederive_slice_a.py: 125 candidates; count_float at tol 1e-12, 1e-9, 0 gives 0 (equilibrium) and 2 (endowment); count_dec with 60-digit Decimal logs gives 0 and 2 (archived {OUTS}/rederive.out)."),
    "E4a-r8-rederive-numbers": ("PASS", f"{SCR}/rederive_slice_a.py: 51 PASS lines covering index, L01 to L03 numbers (archived {OUTS}/rederive.out)."),
    "E4a-r8-concept-anchors-owners": ("PASS", "data-concept uses in index and L01 to L03 match the owners (structure_slice_a.py): e.g. utility-maximization, competitive-equilibrium, pareto-efficiency, externality (E1); expected-utility (E3); lagrange-multiplier, kkt-conditions (M7); derivative, gradient (M2); linear-map, vector-space (M3); random-variable, expectation, conditional-expectation-elementary (M4)."),
    "E4a-r8-macros-and-symbols": ("PASS", "Macros in index and L01 to L03 math: \\E, \\Prob, \\R only among the registered macros; no reserved symbol (see E4a-r6-notation-registered-symbols)."),
    "E4a-r8-data-labs-simulated-labels": ("PASS", "index: no simulation in the hub's own text; labs L01 to L05 and L09 use no draws (grep 'random' in twins gives no draw in L01 to L03, L04 to L05 and L09 docstrings say 'no random draws'); L06 Part E, L07 Part F, L08 Part A seeded and labelled SIMULATED (see E4a-r7-data-simulated-labels)."),
    "E4a-r8-page-smoke-no-external": ("PASS", f"page_smoke PASS for index, L01 to L03 (archived {OUTS}/page_smoke.txt). grep -c 'https?://' on index, L01, L02, L03: 0 each (no external request, no CDN)."),
    "E4a-r9-math-L01-def-1-2-probability": ("PASS", "L01 line 67 (Def 1.2 claim): Prob(X = x_s) equals pi_s exactly when no other state has the same payoff; with pi_t > 0 this is the sum over tied states, read correct."),
    "E4a-r9-prose-L02-meta-description": ("PASS", "L02 line 7 meta description: 'Two-agent Arrow–Debreu exchange economies, budget sets and demands, Walras' law from binding budgets, the closed-form equilibrium with logarithmic utility, and the scale invariance of demand.' Each named item is a lesson section (Prop 2.5, Prop 2.9, Remark 2.10)."),
    "E4a-r9-structure-L03-canon-limits": ("PASS", "L03 lines 264 to 273 (Where the canon breaks): efficiency is not fairness, equilibrium taken as given (A5), complete AD markets, complete preferences, no externalities or frictions, interior equilibria only for (b). Each limit matches a hypothesis or a definition in §1 and §2."),
    "E4a-r10-delta-index-L38": ("PASS", "index line 38 (Data meta-row), re-read and checked against the twins (see E4a-r8-delta-index-data)."),
    "E4a-r10-delta-index-L167": ("PASS", "index line 167 (Data status paragraph), re-read; same claims as line 38; checked against the twins."),
    "E4a-r10-delta-L01-L67": ("PASS", "L01 line 67 (Definition 1.2), re-read (see E4a-r9-math-L01-def-1-2-probability)."),
    "E4a-r10-delta-L01-L155": ("PASS", "L01 line 155 (Remark 1.11): Part D numbers 340/3 and 235/4 re-derived; the claim that the prices differ from the probabilities is correct (see E4a-r6-math-L01-remark111)."),
    "E4a-r10-delta-L01-L287": ("PASS", "L01 line 287 (canon-breaks item 1, finite states): read; consistent with R1 at line 394."),
    "E4a-r10-delta-L01-L322": ("PASS", "L01 line 322 (M1 solution): 55/3 = 18.33 (two decimals stated), 25/2 = 12.5, 35/6 difference (rederive_slice_a.py PASS)."),
    "E4a-r10-delta-L01-R1": ("PASS", "L01 lines 395 to 397 (R1 problem and solution) re-read this round; consistent with canon item 1 (line 287)."),
    "E4a-r10-delta-L02-L7": ("PASS", "L02 line 7 (meta description), re-read (see E4a-r9-prose-L02-meta-description)."),
    "E4a-r10-delta-L02-L348": ("PASS", "L02 line 348 (canon item 3: 'The logarithm is one utility'): the utility -1/x on (0, infinity) is strictly increasing, strictly concave and differentiable, so it satisfies A4; its FOC pi_s/x_s^2 = mu q_s differs from Prop 2.8's, as stated."),
    "E4a-r10-delta-L03-L270": ("PASS", "L03 line 270 (canon item 4: complete preferences): the sentence states the theorem's dependence on the utility representation of A4; read, no overreach beyond the stated assumptions."),
    "E4a-r10-cmd-run_graders": ("PASS", f"`.venv/bin/python tools/run_graders.py --unit E4 --seeds 0-49`: 'run_graders E4: PASS (reference 50/50 seeds, slowest 0.2 s)', rc 0 (archived {OUTS}/run_graders.txt; cross-slice)."),
    "E4a-r10-scan-notation": ("PASS", "Notation scan (see E4a-r6-notation-macros and E4a-r6-notation-registered-symbols): index and L01 to L03 use only registered macros; local symbols (pi, e, u, theta, psi, zeta, mu, lambda, Omega) are not registered."),
    "E4a-r10-structure-script": ("PASS", f"{SCR}/structure_slice_a.py (archived {OUTS}/structure.out): counts, word limits, tiers, quiz, misconceptions, dfn and link checks; all structural checks PASS in the current run (the first run printed nine FAIL lines that were scanner false positives: '...' inside Python code, 'round' inside rounded/rounding, and Greek or standard TeX symbols the registry does not list; the scanner now reads prose only, uses whole-word matching and allows those standard symbols)."),
    "E4a-r10-rederive-script": ("PASS", f"{SCR}/rederive_slice_a.py (archived {OUTS}/rederive.out): 51 PASS, 0 FAIL; the grid counts 0 and 2 are stable under three tolerances and exact-sign Decimal logs."),
    "E4a-r10-ellipsis": ("PASS", "No literal ellipsis in prose. The three-dot sequence occurs only in Python code (`tuple[Fraction, ...]`, twin and page code) and as TeX \\ldots in math. Banned-string scan (structure.out) finds no ellipsis in prose."),
    "E4a-r10-embed": ("PASS", f"{SCR}/lab_page_twin_check.py: each embedded block equals its twin and its output (30 PASS). The embedding still matches for L01 Part E, but its label is wrong: see E4a-r11-lab-L01-partE-label."),
    "E4a-r10-hub-quiz-skill": ("PASS", "index lines 116 to 133 (the two data-skill items). Rung-1 item (line 117): stated gap signs are a hypothetical; the rung-1 instance prints gap(0) = +0.053 and gap(1) = -0.081, and its first bracket is [0.5, 1] (project lab output), which differs from the item's hypothetical pattern. The item states its own pattern, so it is not a false claim (see notes)."),
}

# New rows (round 11), with statuses.
new_rows = [
    {
        "id": "E4a-r11-delta-L02-L568",
        "check": "2.9-prose / cross-reference",
        "location": "L02.html line 568 (quiz item L02q9 explanation)",
        "status": "FAIL",
        "evidence": (
            "The explanation reads 'The proposition is a construction for logarithmic utility (§5), and existence for "
            "general economies is named as a hypothesis (Assumption A5).' In L02 §4 'An equilibrium in closed form' (line 166, "
            "<h2 id=\"s4\">) holds Proposition 2.9, and §5 is 'Where the canon breaks' (line 344). The reference points to the wrong "
            "section. Found by reading the delta hunk (git diff 00a84795..11d7077 hunk at L02 line 568) and the section-number "
            "spans (grep 'section-number' L02.html)."
        ),
        "fix": "L02.html line 568: change '(§5)' to '(§4)'. No other change; the sentence is otherwise correct.",
    },
    {
        "id": "E4a-r11-lab-L01-partE-label",
        "check": "2.5-labs / 2.9-prose",
        "location": "tests/labs/E4/lab-E4-L01-1.py line 94 (label 'short'); course/modules/E/E4/L01.html line 280 (expected output)",
        "status": "FAIL",
        "evidence": (
            "Part E tests (1/8, 3/8, 3/8, 1/4), whose entries sum to 9/8 (page hypothesis L01.html line 160 says '...sum to 9/8', "
            "which is correct; the twin's own docstring line 172 says 'do not sum to 1'). The label passed to the printed line is "
            "'short', so the expected output reads 'rejected short message state probabilities must sum to 1' (L01.html line 280; "
            "run of the twin under -I -W error this round). A vector whose sum exceeds 1 is over, not short, so the printed label "
            "is wrong in the code and in the embedded output. Found by the lab page-versus-twin check and by re-deriving the sums "
            "(rederive_slice_a.py 'L01 Part E short vector sums to 9/8' PASS)."
        ),
        "fix": (
            "In tests/labs/E4/lab-E4-L01-1.py line 94 rename the label 'short' to 'overweight' (or 'sum_not_one'), then run "
            "`.venv/bin/python tools/embed_labs.py course/modules/E/E4/L01.html --refresh lab-E4-L01-1`, then "
            "`.venv/bin/python tools/run_labs.py --unit E4 --page L01`. The hypothesis text stays as it is."
        ),
    },
    {
        "id": "E4a-r11-delta-index-L50",
        "check": "2.9-prose",
        "location": "index.html line 50 (objective 1)",
        "status": "PASS",
        "evidence": "Read this round: 'Decompose ... and value it under the linear valuation of Assumption A2 in Lesson 1.' Matches L01 Assumption A2 (line 99) and Prop 1.7.",
    },
    {
        "id": "E4a-r11-delta-index-L63",
        "check": "2.9-DAG",
        "location": "index.html line 63 (Prerequisites paragraph, M3 sentence)",
        "status": "PASS",
        "evidence": "Read this round: 'From M3 it uses linear maps and vector spaces.' The orthogonal-projection link is removed; no lesson links orthogonal-projection (grep this round). This is the fix for E4a-r6-hub-prereq-usage.",
    },
    {
        "id": "E4a-r11-delta-index-L141",
        "check": "2.9-prose",
        "location": "index.html line 141 (L01 card body)",
        "status": "PASS",
        "evidence": "Read this round: 'under the linear valuation of Assumption A2 in Lesson 1.' Matches L01 line 99.",
    },
    {
        "id": "E4a-r11-delta-index-L38-parts",
        "check": "2.5-labs / 2.2-numbers",
        "location": "index.html line 38 and line 167 (data claims listing parts of L06, L07)",
        "status": "PASS",
        "evidence": "Checked against the twins this round: L06 Parts A to D exact (lab-E4-L06-1 docstring line 211 'Parts A to D are exact'; output lines show 3/7, 6/7, 7/9, 1/3 Fractions); L07 Parts A to E exact (output 'rho2_from_moments 1/3 ...', Part B-D Fractions; docstring line 18 'to float for comparison with the sample' applies to Part F only); L08 Parts B to D double precision (docstring line 5); L09 Fraction; L03 Part B float.",
    },
    {
        "id": "E4a-r11-delta-L01-L7",
        "check": "2.9-prose",
        "location": "L01.html line 7 (meta description)",
        "status": "PASS",
        "evidence": "Read this round: 'under the linear valuation of Assumption A2.' Matches the lesson.",
    },
    {
        "id": "E4a-r11-delta-L01-L109",
        "check": "2.9-prose / notation",
        "location": "L01.html line 109 (Definition 1.6 closing sentence)",
        "status": "PASS",
        "evidence": "Read this round: 'The vector q is called the Arrow–Debreu security price vector.' The plan forbids 'state price' (owned by AP1); the phrase is not used (grep 'state price' 0 hits). The term is not a registered symbol.",
    },
    {
        "id": "E4a-r11-delta-L02-L349",
        "check": "2.4-math / prose",
        "location": "L02.html line 349 (canon item 4)",
        "status": "PASS",
        "evidence": "Re-read this round; see E4a-r8-delta-L02-canon.",
    },
    {
        "id": "E4a-r11-delta-L03-L361",
        "check": "2.4-math / 2.5-labs",
        "location": "L03.html line 361 (E2 solution)",
        "status": "PASS",
        "evidence": "Read this round: the witness gain is stated as (1/4) ln(4/3) > 0 for each agent, 'checked by hand (grade T)'. Re-derived: agent 1 (3,4,1) to (2,4,3) changes utility by (1/2)ln2 - (1/4)ln3 = (1/4)ln(4/3); agent 2 (1,4,3) to (2,4,1) by the same amount (rederive_slice_a.py 'L03 E2 witness gain' PASS). Lab 3 prints the improvement at endowment (line 259, 260). This is the fix for E4a-r8-delta-L03-E2.",
    },
    {
        "id": "E4a-r11-hub-skill-rung1",
        "check": "2.9-prose / 2.5-labs",
        "location": "index.html line 117 and line 123 (rung-1 skill check and explanation)",
        "status": "PASS",
        "evidence": "The item states its own hypothetical gap pattern (positive at 0, negative at 1 and at 1/2), and the explanation (line 123) names the bracket and says the rung-1 example prints the bracket after the first three halvings. project.html lab-E4-project-1 output (this round): bracket after halving 1 [0.5, 1], after 2 [0.5, 0.75], after 3 [0.5, 0.625]; the printed rung-1 instance has gap(0) = +0.053, gap(1) = -0.081 and so gap(0.5) > 0, opposite to the hypothetical pattern. The item does not claim the pattern holds for the rung-1 instance, so no false statement is made; recorded as a note for the owner of slice b.",
    },
    {
        "id": "E4a-r11-cmd-verify_refs-offline",
        "check": "2.1-refs",
        "location": "tools/verify_refs.py --offline (whole registry)",
        "status": "PASS",
        "evidence": f"Output 'offline integrity: 560 entries, 0 problems', rc 0 (archived {OUTS}/verify_refs.txt). `--unit E4` is a live run and was not executed; no network access was used (see E4a-r6-cmd-verify_refs).",
    },
    {
        "id": "E4a-r11-cmd-structure-script",
        "check": "2.9-structure",
        "location": "index.html, L01.html, L02.html, L03.html",
        "status": "PASS",
        "evidence": f"{SCR}/structure_slice_a.py (corrected, see E4a-r10-structure-script): 168 PASS lines, 0 FAIL, exit 0. Archived {OUTS}/structure.out.",
    },
]

rows = []
for rid, prow in prev_rows.items():
    entry = carried[rid]
    status, evidence = entry[0], entry[1]
    loc = entry[2] if len(entry) > 2 else prow["location"]
    rows.append(
        {
            "id": rid,
            "check": prow["check"],
            "location": loc,
            "status": status,
            "evidence": f"Round 11 (pin 11d7077, re-verified): {evidence}",
        }
    )
rows.extend(new_rows)

missing = [rid for rid in prev_rows if rid not in carried]
assert not missing, missing
assert len({r["id"] for r in rows}) == len(rows), "duplicate ids"

# Notes and fields
frag = {
    "unit": "E4",
    "slice": "a",
    "round": 11,
    "verifier": "Haiku independent verifier, E4-a round 11 (did not build E4; no shared context with the builders)",
    "pin": "11d7077a290f7960b183d3a5a6631af4773888f9",
    "base": "00a84795f276456fce19d4181373cc4efba11a36 (round-10 pin). Slice-a delta: index.html (12 lines), L01.html (4), L02.html (4), L03.html (2); lab twins L01 to L03 unchanged. Every hunk read; see E4a-r11-delta-* rows.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE11-E4-a (detached at 11d7077, .venv symlinked)",
    "scratch": "/tmp/e4-v/a-r11/",
    "verified_at": "2026-11-05T11:04:33+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice a has no project grader: mutation testing and the ten student-error mutants and five alternatives do not apply (plan ruling: lab twins are demonstrations; mutation applies to project graders only). mutants is empty.",
        "Two FAIL rows, both small and exact: E4a-r11-delta-L02-L568 (section reference §5 should be §4) and E4a-r11-lab-L01-partE-label (label 'short' for a sum of 9/8). Both are local edits; the second needs embed_labs --refresh.",
        "The round-10 FAIL rows are fixed and verified: E4a-r6-hub-prereq-usage (index line 63 no longer claims orthogonal projection) and E4a-r8-delta-L03-E2 (L03 line 361 now states the checked witness gain (1/4) ln(4/3)).",
        "Observation, not a row (no rule violated): local symbols overlap across lessons. s is a state index in L01 to L03 and a signal in the plan's L05 to L07; u is a utility u_i in L02 to L03 and the noise supply in L06; mu is the KKT multiplier in L02 where the plan lists a mean; eps is a perturbation in L03 Prop 3.4 (b) and signal noise in L06 to L07. None is a registered symbol, and each is defined in its own lesson. The owners of slices b and c may wish to add a local-symbol note to the plan.",
        "Observation: the hub overview (index lines 33, 139, 149) uses 'noise traders', 'informed fraction', 'posteriors' before their lesson definitions. The hub is an overview, not a lesson; no rule in BUILDER_RULES 4.2 applies to it.",
        "Observation: the rung-1 placement item (index line 117) states a gap pattern that differs from the rung-1 instance's printed sign at 0.5 (see E4a-r11-hub-skill-rung1). Not a false claim, since the item states its own hypothetical; the owner of slice b may want the item to say so.",
        "Observation: the name 'Grossman–Stiglitz paradox' appears in the hub and in L08's title as the curriculum's lesson name. No registry key is cited for it in slice a; no bibliographic claim is made.",
        "Not checked: a live verify_refs --unit E4 run (network); the E4 pages cite no registry key, so none is in scope. No screenshot diff was taken; page_smoke geometry and console checks only. The tools/embed_labs.py output was not re-run (it would rewrite files; the verifier does not edit).",
        "The hub's skill item and the hub's data claims about L04 and L05 were checked against twin outputs for Fraction usage only (their proofs are slices b and c).",
    ],
    "summary": "",
}
n_pass = sum(1 for r in rows if r["status"] == "PASS")
n_fail = sum(1 for r in rows if r["status"] == "FAIL")
n_unv = sum(1 for r in rows if r["status"] == "UNVERIFIABLE")
frag["summary"] = (
    f"Slice a (index.html, L01-L03, lab twins L01-L03), round 11 at 11d7077: {len(rows)} rows, {n_pass} PASS, {n_fail} FAIL, "
    f"{n_unv} UNVERIFIABLE. FAIL: L02.html line 568 quiz explanation cites §5 for Proposition 2.9 (should be §4); "
    "lab-E4-L01-1 Part E labels a sum-9/8 vector 'short' in the code and in the expected block. Round-10 FAILs fixed."
)
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(frag, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", OUT, "rows", len(rows), "pass", n_pass, "fail", n_fail)
