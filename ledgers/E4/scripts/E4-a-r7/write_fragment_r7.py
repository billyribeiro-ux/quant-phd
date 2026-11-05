"""Writes ledgers/E4/E4-a.json for the E4 slice a verifier, round 7. Row evidence cites the scripts and outputs under ledgers/E4/scripts/E4-a-r7/."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
S = "ledgers/E4/scripts/E4-a-r7/"
rows: list[dict[str, str]] = []


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str | None = None) -> None:
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix or ""
    rows.append(r)


CARRY_NOTE = "Re-verified in round 7 (subject changed or re-read in full): "

# ---- commands
row("E4a-r6-cmd-check_pages", "2.9-structure", "index.html, L01.html, L02.html, L03.html", "PASS",
    f"Run this round: .venv/bin/python tools/check_pages.py --unit E4 printed 'check_pages E4: PASS' (exit 0); {S}check_pages_E4.out.")
row("E4a-r6-cmd-check_dag", "2.9-DAG", "index.html, L01-L03", "PASS",
    f"Run this round: tools/check_dag.py --all printed 'check_dag E4: PASS' (line for E4 in {S}check_dag.out; exit 0).")
row("E4a-r6-cmd-run_labs", "2.5-labs", "tests/labs/E4/lab-E4-L01-1.py, L02-1.py, L03-1.py", "PASS",
    f"Run this round: tools/run_labs.py --unit E4 printed 'run_labs E4: PASS (12/12)' (exit 0); {S}run_labs_E4.out.")
row("E4a-r6-cmd-page_smoke", "2.9-smoke", "index.html, L01.html, L02.html, L03.html", "PASS",
    f"Run this round alone: tools/page_smoke.py --unit E4 --pages index.html L01.html L02.html L03.html printed 'page_smoke E4: PASS' (exit 0); {S}page_smoke_E4_abc.out.")
row("E4a-r6-cmd-twins-alone", "2.5-labs", "tests/labs/E4/lab-E4-L01-1.py, L02-1.py, L03-1.py", "PASS",
    f"Run this round from cwd /tmp: python -I -W error on each twin by absolute path: exit 0, stderr empty (twin-L01-1/L02-1/L03-1.out and .err in {S}).")
row("E4a-r6-cmd-twin-embed", "2.5-labs", "L01.html, L02.html, L03.html data-run code and pre.expected", "PASS",
    f"{S}check_twins_embed.py (output {S}check_twins_embed.out): code equals the twin file (trailing newline excluded, as the embed tool strips it) and expected equals the twin's stdout, True for L01, L02, L03; ALL_OK.")
row("E4a-r6-cmd-ruff", "tooling", "tests/labs/E4 twins L01-L03", "PASS",
    f"ruff check on the three twins: All checks passed!; ruff format --check: 3 files already formatted ({S}ruff_twins.out).")
row("E4a-r6-cmd-mypy", "tooling", "tests/labs/E4 twins L01-L03", "PASS",
    f"mypy --no-incremental on the three twins: Success, no issues found in 3 source files, exit 0 ({S}mypy_twins.out).")
row("E4a-r6-cmd-pytest", "tooling", "tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py", "PASS",
    f"python -m pytest -q on the three files: all dots, exit 0 ({S}pytest_relevant.out).")
row("E4a-r6-cmd-verify_refs", "2.1-refs", "index.html, L01-L03 (data-references empty)", "PASS",
    f"tools/verify_refs.py --offline: offline integrity 560 entries, 0 problems, exit 0 ({S}verify_refs_offline.out). The slice cites no registry key, so no live resolution is owed.")
row("E4a-r6-cmd-check_projects", "2.6-gate", "course/modules/E/E4/project.html (outside this slice)", "PASS",
    f"tools/check_projects.py --all exit 0 (last line 'check_projects PC3: PASS'; {S}check_projects_all.out). Run for the gate only; project content belongs to another slice.")

# ---- structure
row("E4a-r6-struct-lesson-order", "2.9-structure", "L01.html, L02.html, L03.html", "PASS",
    "Section order read in each file: why-it-matters, numbered sections, the lab section before canon-breaks (L01 line 158 before 284; L02 192 before 343; L03 122 before 264), misconceptions, problem set, key results, retrieval quiz, references, lesson nav.")
row("E4a-r6-struct-counts", "2.9-structure", "L01-L03 misconceptions, problems, quiz", "PASS",
    f"{S}structure_counts_r7.out: each lesson has 3 misconceptions, 12 problems (M1-M3, P1-P3, E1-E3, R1-R3), 9 quiz items with 9 explanations (range 8-15 met).")
row("E4a-r6-struct-why-words", "2.9-structure", "L01 line 51, L02 line 51, L03 line 51", "PASS",
    f"why-it-matters word counts 108, 117, 120 ({S}structure_counts_r7.out); all at most 120 words.")
row("E4a-r6-struct-solution-words", "2.9-structure", "L01-L03 details.solution blocks", "PASS",
    f"Every solution has at least 15 words: minimum 48 (L01), 48 (L02), 20 (L03 R3) in {S}structure_counts_r7.out.")
row("E4a-r6-hours-arith", "2.9-hours", "index.html lines 29, 40-43, 139; L01-L03 line 2 and eyebrow", "PASS",
    "index data-hours-lessons=72, data-hours-project=28, sum 100 (grep output); curriculum.json E4 hours 100 and tier M (python read); 9 lessons x 8 h = 72; each lesson data-hours=8 and eyebrow '8 study hours'; bars 72% and 28%.")

# ---- hub
row("E4a-r6-hub-placement", "2.9-structure", "index.html lines 66-135", "PASS",
    f"Eight placement items: six non-skill, two data-skill items (7, 8). Mastery 0.8. Numeric answers 6 and 8 re-derived ({S}rederive_E4a_r7.out). 6/8 = 75% and 7/8 = 87.5% re-derived; 80% of 8 = 6.4, so seven correct is needed. Item 7 (rung-1 skill check): gap signs at 0, 1/2, 1 are +, -, - so the kept bracket is [0, 1/2] (item text and explanation agree).")
row("E4a-r6-hub-titles", "2.9-structure", "index.html lines 129-149; L01-L09 h1", "PASS",
    "Hub card titles equal each lesson h1 for L01-L09 (grep: 'Arrow–Debreu securities and state-contingent payoffs', 'Arrow–Debreu equilibrium', 'The first welfare theorem', 'Complete and Incomplete Markets', 'Rational-Expectations Equilibrium', 'Noisy rational-expectations equilibrium', 'Price informativeness', 'The Grossman–Stiglitz Paradox', 'The No-Trade Theorem').")
row("E4a-r6-hub-unlocks", "2.9-structure", "index.html line 36", "PASS",
    "curriculum.json: concepts whose prerequisites contain E4 are AP1, AP6, MS1, SR1 (python walk); titles match the hub line: AP1 'No-Arbitrage & the Stochastic Discount Factor', AP6 'Intermediary & Institutional Asset Pricing', MS1 'Microstructure Theory', SR1 'Runs, Liquidity & Fire Sales'.")
row("E4a-r6-hub-prereq-titles", "2.9-structure", "index.html line 35", "PASS",
    "curriculum.json titles: E2 'Game Theory & Information Economics', E3 'Decision Theory Under Risk & Ambiguity', M7 'Optimization'; E4 prereqs ['E2','E3','M7'] (python read); matches the hub.")
row("E4a-r6-hub-KKT-claim", "2.4-math", "index.html line 63; L02.html line 37 (Uses meta) and line 164", "PASS",
    "Hub says E4 uses KKT conditions from M7. L02 line 37 links kkt-conditions in its Uses meta and line 164 uses it (KKT paragraph). Re-derived there: pi_s/x*_s = mu q_s with mu = 1/w; mu(q.x - w) = 0 (budget binds); nonnegativity multipliers zero since x*_s > 0 (rederive script, L02 KKT check).")
row("E4a-r6-hub-prereq-usage", "2.9-DAG", "index.html line 63 against L01-L09 text", "PASS",
    "Each concept the hub names is used on the page it names: utility maximization, competitive equilibrium (L02 Def 2.2), Pareto efficiency and externality (L03 Def 3.2 and canon-breaks), expected utility (L02 A4 and Def 2.2 context), certainty equivalent and Arrow-Pratt (L08 concept links), adverse selection (L09), Lagrange and KKT (L02), random variable, expectation, variance, correlation, normal distribution, conditional expectation (L05-L09), linear map and vector space (L01, L04), derivative and gradient (L02, L03). Observation, not a FAIL: 'orthogonal-projection' is named in the hub's M3 list, but no E4 page links that concept; L06 Lemma 6.4 states an uninformed linear projection in prose (L06 is another slice).")
row("E4a-r6-hub-numbers", "2.2-numbers", "index.html lines 7, 31, 33, 40-43, 68, 71-73, 113-120, 139", "PASS",
    "100 hours, 72 and 28 hours, 28 percent, 80 percent mastery, seven of eight and 87.5 percent re-derived (rederive_E4a_r7.out); all match curriculum.json and the lessons.")
row("E4a-r6-hub-objectives", "2.9-structure", "index.html lines 50-57", "PASS",
    "Each objective names a lesson whose content it describes: 1 L01 (decomposition, A2 valuation); 2 L02 (log equilibrium, budgets, market clearing); 3 L03 (first welfare theorem, MRS check); 4 L04 (payoff-matrix rank: 'rank' 91 hits in L04); 5 L05 (fixed point: 36 hits); 6 L06 and L07 (coefficients, correlation); 7 L08 (bisection: 15 hits); 8 project (solver and report).")
row("E4a-r6-hub-card-claims-L01-03", "2.9-structure", "index.html lines 141-143", "PASS",
    "L01 card: payoff vectors, decomposition, linear valuation under A2 (matches L01 Props 1.4, 1.7). L02 card: budgets, Walras law from binding budgets (Prop 2.5), closed form with logarithmic utility (Prop 2.9), two-agent example checked exactly (Example 2.11, Lab 2). L03 card: feasible allocations, Pareto improvements, MRS between states, proof of no Pareto improvement (Prop 3.4 (a)), equality of MRS with price ratio (Prop 3.4 (b)).")
row("E4a-r6-data-none", "2.2-numbers / 2.5-labs", "index.html line 38 and lines 165-168; L01-L03 lab sections", "FAIL",
    "Hub line 38 says 'Data: none. The labs compute from exact formulas and from fixed inputs', and lines 167 says 'The labs compute from exact formulas and from fixed inputs written into their code'. Three labs also draw seeded samples in code: lab-E4-L06-1.py line 177 (random.Random(SEED)), lab-E4-L07-1.py line 164, lab-E4-L08-1.py line 93; their pages label those parts SIMULATED. So the hub sentence is false for L06 to L08. No real dataset is named (true; the curriculum names none). L01-L03 use no random draws (the twins' docstrings say so; grep for random finds only the phrase).",
    "index.html line 38 and line 167: replace 'The labs compute from exact formulas and from fixed inputs' with 'The labs compute from exact formulas and fixed inputs, and labs L06, L07 and L08 each add one seeded simulation labelled SIMULATED'.")
row("E4a-r6-references-none", "2.1-refs", "L01-L03 section 9; index", "PASS",
    "Each lesson states it cites no registry source; <ol data-references> is empty in L01, L02, L03 (structure_counts_r7.out: 0 entries); the hub has no data-references; no author, year or bibliographic claim appears in the slice (grep).")
row("E4a-r6-dag-closure", "2.9-DAG", "index.html, L01-L03 concept links", "PASS",
    f"Every data-concept used in the slice has an owner in the closure {{E1,E2,E3,M1,M2,M3,M4,M7,P0.1}} per curriculum.json (concept_owners_r7.out): e.g. arrow-debreu-security E4, kkt-conditions M7, externality E1, certainty-equivalent E3, orthogonal-projection M3, adverse-selection E2. Each anchor id exists in course/concepts.html (grep).")
row("E4a-r6-dag-defs-unique", "2.9-DAG", "L01.html line 74, L02.html line 89, L03.html line 78", "PASS",
    "Each of arrow-debreu-security, arrow-debreu-equilibrium and first-welfare-theorem is defined once with a dfn data-concept in its assigned lesson (grep of dfn tags). Internal links L01.html#def-arrow-debreu-security (L02 line 37, L03 line 37) and L02.html#def-arrow-debreu-equilibrium (L03 line 37) resolve.")
row("E4a-r6-dag-D-terms", "2.9-DAG / define-before-use", "index.html, L01-L03", "PASS",
    "Plan D-term grep over the slice (python count): 'state price', 'Bayes', 'martingale', 'common knowledge', 'Banach', 'intermediate value', 'informationally efficient', 'CARA', 'law of one price', 'efficient markets', 'risk-neutral', 'pricing kernel' all 0. Observation, not a FAIL: 'posterior' (hub card L09 text), 'informed fraction' (hub lede, objectives, lessons list) and 'noise trader' (hub) are named in the hub before the lessons define them; 'stochastic discount' and 'no-arbitrage' appear only as the AP1 course title in the hub unlock line.")
row("E4a-r6-notation-macros", "2.4-notation", "index.html, L01-L03 math", "PASS",
    "No \\mathbb in any slice page (grep 0). Custom macros used: \\R (L02 line 55, L03 lines 59, 64) and \\E (L01 lines 138, 150), both registered in notation/notation.json (macros, lines 5-8 and 25-28). The other commands are standard TeX (\\iota, \\Omega, \\bar, \\mathrm, \\pi, \\varepsilon, \\theta, \\tfrac).")
row("E4a-r6-notation-registered-symbols", "2.4-notation", "index.html, L01-L03", "PASS",
    "Registered symbols T, Phi, gamma, R^ast, R^{e ast}, R_f and \\mathbb{Q} (notation.json symbols) do not appear in the slice math (grep over the four pages: no \\Phi, \\gamma, \\ast, \\mathbb, and no math symbol T). S is the conventionally local letter for the state count, defined at L01 Def 1.1 (\\Omega = {1,...,S}).")
row("E4a-r6-notation-e-collision", "2.4-notation", "L02.html line 55; L03.html lines 55, 105, 335", "PASS",
    "e_s (security, Def 1.3) appears in L03 only at line 105 (proof of (b)) and in the sentence at line 55 that names it; the other hits at L03 line 335 are \\bar e_s and \\bar e_t. L02 has no bare e_s (grep: every hit is \\bar e_s or e^i_s). L02 line 55 now says the superscript e 'names an endowment in this lesson' and L03 line 55 says e^i is an endowment.")
row("E4a-r6-notation-mu-local", "2.4-notation", "L02.html line 164", "PASS",
    "mu appears in the KKT paragraph as the multiplier. mu is not registered in notation.json (notation.json:3 lists mu among the conventionally local letters). Observation: the sentence that first displays mu uses it before the words 'the multiplier mu = 1/w' in the same paragraph; the reader can see it is the KKT multiplier from the sentence before.")
row("E4a-r7-notation-u-local", "2.4-notation", "L02.html lines 68-71 (u_i); L03.html line 69 (u_i); L06.html (noise supply u)", "PASS",
    "Observation, not a FAIL: u_i is the utility of agent i in L02-L03; the lowercase bare u is the noise-trader supply in L06 (grep). 'u' is not registered in notation.json, and the plan lists both as local letters, so no rule in the notation registry is broken; the builder may wish to rename the utility to something else, but none is required by the verifier rules.")
row("E4a-r6-banned-phrases", "2.9-prose", "index.html, L01-L03", "PASS",
    f"{S}structure_counts_r7.out: no BANNED string (TODO, TBD, lorem, for brevity, clearly, obviously, studies show, experts agree, it is important to note, ...) outside code blocks. The only ellipses are inside Python code blocks.")
row("E4a-r6-process-words", "2.9-prose", "index.html, L01-L03, lab twins", "PASS",
    f"{S}structure_counts_r7.out: no 'round', 'builder', 'verifier', 'unit report' or 'REQUEST' as a process word; the one 'round' hit is 'rounded' in L01 line 386. Grep of the twin docstrings: no process word.")
row("E4a-r6-scope-words", "2.4-math / prose", "index.html, L01-L03 (every, all, always, only, any, same, exactly, never)", "PASS",
    "Each scope claim checked: L01 line 62 ('every result ... that writes a sum over states uses A1': Props 1.4, 1.7, 1.10 cite A1); L01 line 67 ('every claim' Prop 1.4 holds for all of R^S); L02 line 55 ('names an endowment in this lesson' checked by grep); L02 line 94 ('No proposition below proves A5': no proposition states existence); L02 canon 'Full sharing' (P3); L03 line 51 and Prop 3.4 scope are the Lesson L02 economy.")
row("E4a-r6-define-before-use", "2.9-prose", "L01 Def 1.9 before Prop 1.10; L02 Def 2.1 before Def 2.2; L02 Lemma 2.4 defines iota before Prop 2.5; L03 Def 3.1-3.3 before Prop 3.4", "PASS",
    "Terms checked in order: claim (Def 1.2), Arrow-Debreu security (Def 1.3), value V (A2), security price vector (Def 1.6), expected payoff (Def 1.9), budget set and wealth (Def 2.1), demand (Def 2.2), Arrow-Debreu equilibrium (Def 2.3), excess demand z (Def 2.3), interior (dfn in L03 line 51), feasible allocation (Def 3.1), Pareto improvement (Def 3.2), MRS (Def 3.3). Forward pointers in why-it-matters paragraphs name the defining item and are not uses.")
row("E4a-r6-hub-forward-naming", "2.9-prose", "index.html lines 33, 53, 56, 139, 149", "PASS",
    "Observation, not a defect: the hub lede and the lesson list name noise traders, Arrow-Debreu securities, the informed fraction and posteriors before their lessons define them. The hub is an overview; the round-4 and round-5 judgment is kept.")
row("E4a-r6-attribution", "2.1-refs", "index.html, L01-L03", "PASS",
    "No attribution, locator, equation number or date to an outside source appears in the slice. Grep this round: no four-digit year in index, L01, L02 or L03; Muth, Milgrom, Mas-Colell and Whinston do not occur; 'Grossman' occurs only in the hub lede, meta and card titles as the name of the paradox, with no citation. 'Walras' law' and 'first welfare theorem' name results and carry no source.")

# ---- numbers in lessons
row("E4a-r6-num-L01-M1-rounding", "2.2-numbers", "L01.html line 322 (M1 solution)", "PASS",
    "55/3 = 18.33... stated as 'about 18.33 cents to two decimal places': the rule is stated. Expected payoff 12.5 and the difference 35/6 re-derived (rederive_E4a_r7.out).")
row("E4a-r6-num-L01-E3-rounding", "2.2-numbers", "L01.html line 386 (E3 solution)", "PASS",
    "Round-6 FAIL is fixed. Line 386 now reads '340/3 approx 113.33 cents, rounded to two decimal places from 340/3'. 340/3 = 113.333..., so 113.33 is the rounding, and the rule is stated (plan 2.1 item 1). 235/4 = 58.75 exact.")
row("E4a-r6-num-L01-remaining", "2.2-numbers", "L01.html lines 113-161, 262-281, 320-336, 386, 402-404, 447-449, 463, 484-486", "PASS",
    "Re-derived with exact Fractions (rederive_E4a_r7.out, 78 checks, 0 FAIL): 340/3, 56, 596/3, 235/4 (Lab 1 and hypothesis); 55/3, 12.5, 35/6 (M1); -1/8, 11/8, 17/8 (M3); 1/4 and 1 (R2); quiz 4.25, 3, 0.6.")
row("E4a-r6-num-L02-example", "2.2-numbers", "L02.html lines 124-126, 187-190, 299-363, 377-393, 429-443, 506-529", "PASS",
    "theta1 = 9/16, theta2 = 7/16; q* = (1/8, 1/32, 1/16); x1 = (9/4, 9/2, 9/4); x2 = (7/4, 7/2, 7/4); q.ebar = 1; residuals 0; ratios 16/9 and 16/7 equal 1/w; M1 (1, 2), M2 (3/4, 3/8, 3/2), M3 (2,2); quiz 2, 0.125 and 0.0625 (rederive_E4a_r7.out).")
row("E4a-r6-num-L02-remark26", "2.2-numbers", "L02.html line 125", "PASS",
    "At q = (2,1,1): wealths 11 and 9; demands (11/4 x3) and (9/4 x3); excess demand (1,-3,1), unweighted sum -1 and q.z = 0 (rederive_E4a_r7.out).")
row("E4a-r6-num-L02-misconceptions", "2.2-numbers", "L02.html lines 358, 362, 366", "PASS",
    "State 2 price 1/32 vs state 3 price 1/16 (e-bar 8 vs 4); v = (1,-1,0) has q.v = 3/32; e1 costs 9/16 = w1 (rederive_E4a_r7.out).")
row("E4a-r6-num-L03-example36", "2.2-numbers", "L03.html lines 119, 250-254, 303-304, 476", "PASS",
    "MRS agent 1 and agent 2: 12 -> 4, 13 -> 2, 23 -> 1/2; price ratios 4, 2, 1/2; M1 MRS 2 for pi=(1/3,2/3), x=(1,4) (rederive_E4a_r7.out).")
row("E4a-r6-num-L03-R2", "2.2-numbers", "L03.html line 385 (R2 solution, numbers only)", "PASS",
    "Numbers re-derived: endowment MRS 8/3 (agent 1) and 8 (agent 2); derivatives 1/12 and 1/4 along the trade (rederive_E4a_r7.out); the witness (2,4,3), (2,4,1) adds to (4,8,4), and both utilities rise for small eps. The defective compensation sentence in the same solution is a separate row, E4a-r7-math-L03-R2-compensation.")
row("E4a-r6-num-L03-grid", "2.5-labs / 2.4-math", "L03.html lines 124, 258-261", "PASS",
    "Independent grid enumeration in rederive_E4a_r7.py (float, tolerance 1e-9, separate code): 125 allocations, 0 improvements at the equilibrium, 2 at the endowment, first improvement agent 1 (2,4,3) and agent 2 (2,4,1); equilibrium fraction 9/16 is not a grid value. Matches Lab 3 output lines 257-260.")

# ---- math
row("E4a-r6-math-L01-props", "2.4-math", "L01.html lines 77-151", "PASS",
    "Prop 1.4 (decomposition), Prop 1.7 (value formula; induction from A2 with finite sum from A1), Prop 1.8 (uniqueness of prices), Prop 1.10 (value equals expectation iff q = pi): each proof re-read and valid; hypotheses A1 and A2 listed before each statement.")
row("E4a-r6-math-L01-A2-sentence", "2.4-math", "L01.html line 104", "PASS",
    "A2 excludes quantity discounts, bid-ask spreads and price impact because each makes V nonlinear: a discount breaks V(2x) = 2V(x); a bid-ask spread (a long at one price, a short at another) gives V(x)+V(-x) nonzero; price impact makes V depend on size. Reasoning checked.")
row("E4a-r6-math-L01-remark111", "2.4-math", "L01.html line 155", "PASS",
    "Nothing in A1 or A2 forces q = pi: any positive q defines a linear V by Prop 1.7, so (b) of Prop 1.10 is not implied. The printed 'equal_to_expected_payoff False' (Lab 1 line 277) is the evidence.")
row("E4a-r6-math-L01-R1-countable", "2.4-math", "L01.html lines 287, 394-399", "PASS",
    "Coordinate decomposition holds for countable states (one nonzero term in each state); the step that fails is A2 applied to an infinite sum (A2 stated for two terms). The page offers no sufficient condition and says so.")
row("E4a-r6-math-L01-R2-R3-P", "2.4-math", "L01.html lines 345-411", "PASS",
    "P1 (iota = sum of e_s, V(iota) = sum q_s), P2 (V(0)=0, V(-x)=-V(x) from A2 with a=0,b=0 and a=-1,b=0), P3 (q != pi gives V(e1) = 1/4 != 1/3 = E e1; contrapositive of Prop 1.10), R2 (V = (sum q x)^2 gives 1/4 and 1; linearity fails), R3 (nonnegative value iff q >= 0): all re-derived.")
row("E4a-r6-math-L02-lemma-prop25", "2.4-math", "L02.html lines 99-121", "PASS",
    "Lemma 2.4: y = (w/(2 q.iota)) iota has q.y = w/2, is affordable, and has finite utility; a demand with a zero entry has utility minus infinity, so every demand is strictly positive. Prop 2.5 (Walras): budgets bind by A1 strict increase and the perturbation x + delta iota; summing the two budgets gives q.z = 0. Hypotheses A1, A3, A4 cited.")
row("E4a-r6-math-L02-cor27-prop28", "2.4-math", "L02.html lines 128-161", "PASS",
    "Cor 2.7 from q.z = 0 and q_s > 0. Prop 2.8: x*_s = pi_s w/q_s; tangent-line inequality for ln with equality iff x = x* (strict concavity); sum with weights pi_s; pi_s/x*_s = q_s/w; equality forces x = x* since pi_s > 0 (A1); q.x* = w uses sum pi = 1 (A1). Proof complete.")
row("E4a-r6-math-L02-KKT-paragraph", "2.4-math", "L02.html line 164", "PASS",
    "Stationarity pi_s/x_s = mu q_s, dual feasibility mu >= 0, complementary slackness mu(q.x - w) = 0 hold at x* with mu = 1/w; nonnegativity multipliers vanish because x*_s > 0. The sentence states that the proof does not use these conditions and makes no necessity or sufficiency claim.")
row("E4a-r6-math-L02-prop29-remark210", "2.4-math", "L02.html lines 168-185", "PASS",
    "Prop 2.9: theta1 + theta2 = 1; q*.ebar = 1; x_s = theta_i ebar_s is a demand by Prop 2.8 and clears markets; w_i = theta_i. Remark 2.10: scaling (q,w) by psi leaves x unchanged; q* is not shown unique (the page says so). Proof re-derived line by line.")
row("E4a-r6-math-L02-R1-R3-P-M", "2.4-math", "L02.html lines 404-470", "PASS",
    "P1 (Cor 2.7 with s = 3), P2 (scaling psi, bundles unchanged), P3 (x/ebar = theta_i), R1 (I agents, same proof: sums of theta_i = 1), R2 (d x_s/d q_s = -x_s/q_s, elasticity -1; doubling q1 halves x1), R3 (A3 used where: dividing by ebar_s and q*_s, w_i > 0). Consistent with the proofs.")
row("E4a-r6-math-L03-def33", "2.4-math", "L03.html lines 67-74", "PASS",
    "MRS formula pi_s u'(x_s)/(pi_t u'(x_t)) follows from the partial derivatives of U. u' > 0 on (0,inf) by the argument of the (b) proof (nonnegative by strict increase, nonincreasing by concavity, zero would make u constant on an interval, contradicting strict increase). Definition uses strictly positive bundles, as stated.")
row("E4a-r6-math-L03-prop34a", "2.4-math", "L03.html lines 91-101", "PASS",
    "Proof of (a): Step 1 (strict improvement implies q.y > w, else y in B and better than the demand), Step 2 (weak improvement implies q.y >= w, by a small positive shift using A1 and A4), Step 3 (add the two budgets; contradiction with feasibility). Each step valid; hypotheses cited.")
row("E4a-r6-math-L03-prop34b", "2.4-math", "L03.html lines 103-110", "PASS",
    "d = e_s/q*_s - e_t/q*_t has q*.d = 0; derivative of U at 0 is G = pi_s u'(x_s)/q*_s - pi_t u'(x_t)/q*_t (d_s = 1/q*_s, d_t = -1/q*_t); G = 0 by the two-sided sign argument; dividing by pi_t u'(x_t)/q*_t > 0 gives MRS = q*_s/q*_t. Valid.")
row("E4a-r6-math-L03-remark35-P3", "2.4-math", "L03.html lines 113-115, 339-343", "PASS",
    "Remark 3.5 and P3 list the hypotheses each part uses: (a) uses strict monotonicity, A1 and A3 through Lemma 2.4 and q* > 0, no derivative; (b) adds differentiability and the strict positivity of x*. Consistent with the proofs.")
row("E4a-r6-math-L03-R1-free-disposal", "2.4-math", "L03.html lines 375-379", "PASS",
    "The free-disposal argument is valid. The solution names the last step as the one that 'uses the strict positivity of the prices'; that step needs only q* >= 0 (its own sentence says 'because every price is strictly positive' and the argument goes through with weak positivity). Strict positivity enters earlier, through w_i > 0 and Lemma 2.4. Observation, not a FAIL: the wording overstates which part needs strictness.")
row("E4a-r6-math-L03-R3", "2.4-math", "L03.html lines 389-393", "PASS",
    "Boundary argument: a move that lowers a zero entry leaves the orthant and the utility is minus infinity at zero, so the two-sided derivative in (b) does not exist for that move. Lemma 2.4 gives strictly positive equilibrium bundles. Valid.")
row("E4a-r6-math-L03-M-P-E", "2.4-math", "L03.html lines 300-369", "PASS",
    "M1 (MRS 2), M2 (demand (3/2, 3), MRS 2, equals q1/q2 = 2), M3 (feasibility of the split), P1 (no allocation with every agent strictly better off, via Step 1 and the budget sum), P2 (MRS = pi_s ebar_t/(pi_t ebar_s) = q*_s/q*_t, theta cancels), P3 (hypotheses), E1 (printed 4 and 4, price ratio 4), E2 (2 improvements; witness adds to ebar), E3 (grid is 125 points out of a continuum): consistent with Lab 3 output and the proofs.")
row("E4a-r6-math-keyresults", "2.3-grades", "L01 section 7, L02 section 8, L03 section 6 tables", "PASS",
    "Grades T for proved propositions and for exact arithmetic reproduced by labs; C for the grid enumeration with its basis named (L03 key results row 5); consistent with BUILDER_RULES and with the proofs on the page.")
row("E4a-r6-grades-claims", "2.3-grades", "L01-L03 claim spans", "PASS",
    "Propositions graded T have hypotheses listed. The grid counts are graded C with basis. No empirical claim appears on these pages, so no B or A claim requires counter-evidence.")

# ---- labs
row("E4a-r6-lab-L01-hypothesis", "2.5-labs", "L01.html line 160 vs Lab 1 output lines 262-280", "PASS",
    "Hypothesis values 340/3 and 56 cents, linearity with weights 2 and -1/2, 235/4 expected payoff not equal to the value at the prices, rejections for negative entry and entries summing to 9/8 all match the printed output and the re-derivation.")
row("E4a-r6-lab-L01-interpretation", "2.5-labs", "L01.html line 281", "PASS",
    "Part A exact decomposition; Part B values 340/3 and 56; Part C equality 596/3 for one combination ('It checks A2 on that combination only'); Part D False flag; Part E messages. Each sentence matches the output lines 262-280.")
row("E4a-r6-lab-L01-code", "2.5-labs", "lab-E4-L01-1 (L01 lines 161-261; twin tests/labs/E4/lab-E4-L01-1.py)", "PASS",
    "Code read in full: exact Fraction arithmetic; check_probabilities raises ValueError for non-positive entries and for sums not equal to 1; main() called at top level with no __name__ guard; no RNG; stdlib only (fractions). Output reproduced by the twin run.")
row("E4a-r6-lab-L02-hypothesis", "2.5-labs", "L02.html line 194 vs Lab 2 output lines 315-339", "PASS",
    "Aggregate (4,8,4), wealth shares 9/16 and 7/16, prices (1/8,1/32,1/16), q.ebar = 1, demands, residuals 0, ratios 16/9 and 16/7, Part E unchanged demands, Part F ValueError: all match the output.")
row("E4a-r6-lab-L02-interpretation", "2.5-labs", "L02.html line 340 (changed this round)", "PASS",
    CARRY_NOTE + "the new sentence 'with the demands given by the formula of Proposition 2.8, these bundles satisfy Definition 2.3' is correct: Part C checks budgets and market clearing for the formula demands, and Prop 2.8 (proved) makes them demands. 'With wealth held fixed, the demand would fall by a factor of 3' is an exact consequence of x = pi w/q, not printed by the lab; the page does not claim it is printed.")
row("E4a-r6-lab-L02-code", "2.5-labs", "lab-E4-L02-1 (L02 lines 195-314; twin)", "PASS",
    "Code read in full: exact Fractions; check_economy raises ValueError for non-positive endowment entries; demand raises for wealth <= 0; main() top level; no RNG; stdlib fractions only.")
row("E4a-r6-lab-L03-hypothesis", "2.5-labs", "L03.html line 124 vs Lab 3 output lines 250-260", "PASS",
    "Part A prints rates 4, 2, 1/2 for both agents, each flag True; Part B counts 125 grid allocations, 0 improvements at equilibrium, 2 at endowment, first improvement (2,4,3)/(2,4,1); tolerance 1e-12 (TOL in code); no random draws. All match.")
row("E4a-r6-lab-L03-interpretation", "2.5-labs", "L03.html line 261", "PASS",
    "Each interpretation sentence matches the printed lines; the zero count is labelled grade C with its basis (finite enumeration); 'It does not prove efficiency' is consistent with Prop 3.4 (a).")
row("E4a-r6-lab-L03-code", "2.5-labs", "lab-E4-L03-1 (L03 lines 125-249; twin)", "PASS",
    "Code read in full: exact Fractions for Part A; float utilities for Part B with TOL = 1e-12 and an explicit improves() rule (worse only when below by more than TOL, better only when above by more than TOL); product() grid of 5^3 = 125 allocations; main() top level; no RNG.")
row("E4a-r6-lab-page-equals-twin", "2.5-labs", "L01.html, L02.html, L03.html data-run code and pre.expected", "PASS",
    f"{S}check_twins_embed.out: code equals the twin (trailing newline only), expected equals the twin stdout, ALL_OK.")
row("E4a-r6-lab-hypothesis-before-output", "2.5-labs", "L01 line 160, L02 line 194, L03 line 124", "PASS",
    "Each lab's p.hypothesis paragraph precedes its pre.expected block in each lesson (document order read in the three files).")
row("E4a-r6-lab-stdlib-no-network", "2.5-labs", "lab-E4-L01-1, L02-1, L03-1 imports", "PASS",
    "Imports: fractions (L01, L02), math, fractions and itertools (L03). No network call; no NumPy or SciPy.")
row("E4a-r6-lab-main-toplevel", "2.5-labs", "three twins", "PASS",
    "Each twin ends with an unconditional main() call and has no if __name__ guard (grep; read at the file ends).")
row("E4a-r6-lab-runtime", "2.5-labs", "three twins", "PASS",
    "CPython run time under python -I -W error: about 0.01-0.02 s each (/usr/bin/time, this round; time-L0n-1.txt). page_smoke, which loads each page in Chromium and runs its labs, passed (page_smoke_E4_abc.out). Pyodide itself was not run by this verifier; the margin to the 10 s limit is more than two orders of magnitude on CPython.")
row("E4a-r6-lab-no-mutants", "2.5-labs", "lab twins L01-L03", "PASS",
    "Lab twins are demonstrations; mutation testing applies to the project grader only (architect ruling). Slice a has no grader, so no mutants are owed here.")

# ---- quizzes
row("E4a-r6-quiz-hub", "2.9-structure", "index.html lines 66-135 (placement quiz)", "PASS",
    "Eight items with correct answers and explanations that match the lessons and the project (checked item by item: numeric 6, 8; adverse selection E2 L03 (title 'Adverse Selection') and signaling E2 L04 ('Signaling'); Lagrange M7; competitive equilibrium Def 2.2 of L02; linear map; skill check 7 (rung 1) gives bracket [0, 1/2]; skill check 8 (rung 2) gives G = F_U - e^{ac} F_I, which matches project Proposition 3 and the indifference_gap return line at project.html lines 176-181).")
row("E4a-r6-quiz-L01", "2.9-structure", "L01.html lines 437-506 (9 items)", "PASS",
    "Each answer and explanation checked: coefficient 7 (Prop 1.4); value 4.25 (Prop 1.7); 2V(x) (A2); expected payoff 3 (Def 1.9); security property; A1; value 0.6 (Problem P1); r = q (Prop 1.8); size discount (A2, Problem R2).")
row("E4a-r6-quiz-L02", "2.9-structure", "L02.html lines 497-570 (9 items)", "PASS",
    "Answers and explanations checked: pi_s w/q_s (Prop 2.8); demand 2 (Problem M1); q.z = 0 (Prop 2.5); lemma 2.4 explanation; q*_1 = 1/8 (Prop 2.9); w_i = theta_i (proof of Prop 2.9); unchanged under scaling (Problem P2); Definition 2.2; statement about Prop 2.9 (Remark 2.10 and A5).")
row("E4a-r6-quiz-L03", "2.9-structure", "L03.html lines 418-487 (9 items)", "PASS",
    "Answers and explanations checked: Prop 3.4 (a); MRS 2 (Problem M1); Def 3.2 wording; Prop 3.4 (b) hypotheses (Remark 3.5); price ratio 2 (Problem M2); Example 3.6 equal rates at different bundles (Misconception 2); Pareto efficiency (Definition 3.2 and Misconception 1); MRS^1_12 = 4 (Example 3.6, re-derived: (1/2 / 9/4)/(1/4 / 9/2) = 4); the step of the proof of (a) that uses strict monotonicity (Step 2).")
row("E4a-r6-hub-lede-and-ladder", "2.9-structure", "index.html lines 33, 155-161", "PASS",
    "Lede names Lessons 1 to 9 in the right order and the project; the ladder rungs match the project page (rung 1 worked example on one SIMULATED instance; rung 2 completion of the return line of indifference_gap; rung 3 solver.py with solve_model returning informed_fraction, price_informativeness and indifference_gap; rung 4 stretch). Checked against course/modules/E/E4/project.html lines 44-58, 176-181, 310-322.")
row("E4a-r6-observation-noise-e", "2.4-notation", "L02.html line 55", "PASS",
    "Observation (not a row defect): the letter e appears both as the Arrow-Debreu security e_s (L01) and as an endowment e^i (L02 on); the L02 and L03 sentences separate them. Recorded for the builder.")

# ---- new rows for this round
row("E4a-r7-math-L03-R2-compensation", "2.4-math / prose", "L03.html line 385 (R2 solution, agent 1 sentence)", "FAIL",
    f"The sentence reads 'Agent 1 would give up 8/3 units of state 2 for one more unit of state 1, so it would give up one unit of state 1 for only 3/8 units of state 2. The trade gives it 4 units of state 2 for each unit of state 1 it gives up, which is more than 3/8, so agent 1 gains.' The compensation agent 1 needs to give up one unit of state 1 is 8/3, the reciprocal of 3/8 is not the compensation: MRS^1_12 at the endowment = (pi_1/3)/(pi_2/4) = 8/3 (rederive_E4a_r7.out: 'L03 endowment MRS agent1 12 = 8/3'; 'L03 R2 compensation needed by agent 1 is 8/3 (not 3/8)'). Comparing the trade's 4 units with 3/8 would wrongly show a gain for any trade. The previous text (round-6 pin 4bd8cb94, the same line) had 'Agent 1 needs 8/3 units of state 2 to give up one unit of state 1, and the trade gives it 4 units ... so agent 1 gains', which is correct. The round-7 delta introduced the inverted version.",
    "L03.html line 385: replace 'Agent 1 would give up \\(\\tfrac83\\) units of state 2 for one more unit of state 1, so it would give up one unit of state 1 for only \\(\\tfrac38\\) units of state 2. The trade gives it 4 units of state 2 for each unit of state 1 it gives up, which is more than \\(\\tfrac38\\), so agent 1 gains.' with 'Agent 1 needs \\(\\tfrac83\\) units of state 2 to give up one unit of state 1, and the trade gives it 4 units of state 2 per unit, so agent 1 gains.'")
row("E4a-r7-data-simulated-labels", "2.8-data / 2.5-labs", "lab-E4-L06-1.py line 177, lab-E4-L07-1.py line 164, lab-E4-L08-1.py line 93; L06.html line 254, L07.html, L08.html", "PASS",
    "The seeded draws are random.Random(SEED) (grep) and each page labels them SIMULATED (L06 line 240 'SIMULATED: one seeded draw of 20 000 observations', L06 line 254 'SIMULATED. A seeded sample'; L08 docstring 'Part A uses seeded draws and is SIMULATED'). The labelling is present; only the hub's data sentence (row E4a-r6-data-none) is wrong.")
row("E4a-r7-hub-cross-unit-titles", "2.9-DAG / 2.2", "index.html line 63; E2 L03 and L04 h1; E3 index h1", "PASS",
    "E2 L03 h1 'Adverse Selection' and E2 L04 h1 'Signaling' match the placement explanation (index line 82 cites E2 Lesson 3 and Lesson 4). E3 index h1 'Decision Theory Under Risk & Ambiguity' matches the hub prerequisite title.")
row("E4a-r7-delta-coverage", "2.9-scope", "git diff 4bd8cb94..06994db1 for slice a paths", "PASS",
    "Delta: index.html unchanged; tests/labs/E4/lab-E4-L01-1.py, L02-1.py, L03-1.py unchanged (only L07 and project-3 twins changed, out of slice). Slice hunks read and re-verified: L01 line 51 (weighted sum), L01 line 386 (rounding), L02 line 55 (endowment superscript), L02 line 71 (A4 example refers to §3 and §4), L02 line 340 (interpretation), L03 line 385 (R2 solution; defective). All other rows re-verified this round from the whole-file read.")
row("E4a-r7-rederive-all-numbers", "2.2-numbers", "index.html, L01-L03 (every number in prose)", "PASS",
    f"{S}rederive_E4a_r7.py (output {S}rederive_E4a_r7.out): 78 independent exact checks, 0 FAIL, covering L01 Examples, Props and Labs, L02 Example 2.11 and Remark 2.6, L03 MRS values, R2 derivatives, grid enumeration, and hub numbers.")

fragment = {
    "unit": "E4",
    "slice": "a",
    "round": 7,
    "verifier": "Haiku independent verifier, E4-a round 7 (did not build E4; no shared context with the builders)",
    "pin": "06994db16d1ab449bcf29898a7f56cfa999dce57",
    "base": "4bd8cb94a8e171e80c4c34da1b3f32be7cb93f07 (round-6 pin). Delta in the slice: L01 lines 51 and 386; L02 lines 55, 71, 340; L03 line 385. index.html and the three slice twins unchanged.",
    "checkout": str(ROOT),
    "scratch": "/tmp only for the twin runs (cwd /tmp, python -I -W error by absolute path). Scripts and logs under ledgers/E4/scripts/E4-a-r7/.",
    "verified_at": "2026-11-04T22:22:17+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Whole slice read line by line this round: index.html (173 lines), L01.html (524), L02.html (588), L03.html (505) and the three twins. Every hunk of the round-6 to round-7 delta read and re-derived.",
        "Round-6 FAIL E4a-r6-num-L01-E3-rounding is fixed and re-verified PASS.",
        "Two FAILs this round: E4a-r7-math-L03-R2-compensation (L03 line 385, inverted compensation ratio introduced by the delta) and E4a-r6-data-none (hub lines 38 and 167 say the labs use only exact formulas and fixed inputs; L06, L07 and L08 draw seeded samples).",
        "Observations, not FAILs: hub lede and objectives name posteriors, the informed fraction and noise traders before their lessons define them (hub overview, judgment kept from rounds 4-6); 'orthogonal-projection' is named in the hub but no E4 page links it (L06 states the projection in prose); u is used both as agent utility u_i (L02-L03) and as the noise supply (L06); mu first appears as the KKT multiplier before its meaning is stated in the same paragraph; L03 R1 solution says the last step uses the strict positivity of prices, though it needs only nonnegativity.",
        "Mutants: none. Slice a has no grader; lab twins are demonstrations under the architect ruling.",
    ],
    "summary": {},
}

counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
fragment["summary"] = {
    "rows": len(rows),
    "pass": counts["PASS"],
    "fail": counts["FAIL"],
    "unverifiable": counts["UNVERIFIABLE"],
    "mutants_killed": 0,
    "mutants": 0,
}
fragment["verdict"] = "PASS" if counts["FAIL"] == 0 and counts["UNVERIFIABLE"] == 0 else "FAIL"

out = ROOT / "ledgers/E4/E4-a.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(out, counts, fragment["verdict"])
