"""Writes the round-3 verifier fragment for E4 slice a (hub index.html, L01-L03, lab twins).

Keeps every round-2 row id (VERIFIER_RULES; verifier-rules.md) and adds the rows raised in round 3.
Run from the checkout root: .venv/bin/python ledgers/E4/scripts/E4-a-r3/write_fragment.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
L = "ledgers/E4/scripts/E4-a-r3/logs"
S = "ledgers/E4/scripts/E4-a-r3"

rows: list[dict[str, str]] = []


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str = "") -> None:
    item = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        item["fix"] = fix
    rows.append(item)


# ---------------- commands (re-run in round 3 on pin 67a2d13) ----------------
row("E4a-cmd-check_pages-unit", "2.9-structure", "index.html, L01.html, L02.html, L03.html", "PASS",
    f"Re-run: .venv/bin/python tools/check_pages.py --unit E4 -> 'check_pages E4: PASS', exit 0 ({L}/check_pages_unit.txt).")
row("E4a-cmd-check_pages-lessons", "2.9-structure", "L01.html, L02.html, L03.html", "PASS",
    f"Re-run: check_pages.py --unit E4 --page L01, --page L02, --page L03 -> each 'check_pages E4 Lnn: PASS', exit 0 ({L}/check_pages_L01.txt, _L02, _L03).")
row("E4a-cmd-check_dag", "2.9-dag", "all four slice pages", "PASS",
    f"Re-run: tools/check_dag.py --unit E4 -> 'check_dag E4: PASS', exit 0 ({L}/check_dag_E4.txt). Linked uses only; unlinked names checked by grep (E4a-dag-outside-closure).")
row("E4a-cmd-run_labs", "2.5-labs", "tests/labs/E4/lab-E4-L01-1.py, lab-E4-L02-1.py, lab-E4-L03-1.py", "PASS",
    f"Re-run: run_labs.py --unit E4 --page L01 / L02 / L03 -> 'run_labs E4: PASS (1/1)' each, exit 0 ({L}/run_labs_L01.txt, _L02, _L03); whole-unit run_labs.py --unit E4 -> 'PASS (12/12)', exit 0 ({L}/run_labs_E4_whole.txt).")
row("E4a-lab-twins-alone", "2.5-labs", "tests/labs/E4/lab-E4-L01-1.py, lab-E4-L02-1.py, lab-E4-L03-1.py", "PASS",
    f"Each twin run as python -I -W error from cwd /tmp with PATH only: exit 0, stderr 0 bytes (lab-E4-L01-1, lab-E4-L02-1, lab-E4-L03-1). Script {S}/check_twins_embed.py, log {L}/twins_embed.txt, ALL_OK.")
row("E4a-lab-embed-equality", "2.5-labs", "L01.html, L02.html, L03.html (data-run and pre.expected blocks)", "PASS",
    f"{S}/check_twins_embed.py: page data-run code equals the twin source (True x3) and each pre.expected block equals the twin stdout (True x3) ({L}/twins_embed.txt).")
row("E4a-cmd-ruff", "2.5-labs", "tests/labs/E4/lab-E4-L01-1.py, L02-1.py, L03-1.py", "PASS",
    f"ruff check -> 'All checks passed!', exit 0; ruff format --check -> '3 files already formatted', exit 0 ({L}/ruff_check.txt, ruff_format.txt).")
row("E4a-cmd-mypy", "2.5-labs", "tests/labs/E4/lab-E4-L01-1.py, L02-1.py, L03-1.py", "PASS",
    f"mypy --no-incremental on the three twins -> 'Success: no issues found in 3 source files', exit 0 ({L}/mypy_slice.txt).")
row("E4a-cmd-page_smoke", "2.9-smoke", "index.html, L01.html, L02.html, L03.html", "PASS",
    f"page_smoke.py --unit E4 --pages index L01 L02 L03, run alone -> 'page_smoke E4: PASS', exit 0; lab times 0.0 s each; boot 1.1 s ({L}/page_smoke_slice.txt).")
row("E4a-cmd-pytest", "2.5-labs", "tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py", "PASS",
    f"pytest -q on the three modules -> all dots, exit 0 ({L}/pytest_relevant.txt). The full suite was not run.")
row("E4a-cmd-verify_refs", "2.1-citations", "index.html, L01.html, L02.html, L03.html (data-references)", "PASS",
    f"verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0 ({L}/verify_refs_offline.txt). The slice cites no registry key: data-references lists are empty (L01.html line 512, L02.html line 574, L03.html line 493; hub has none; grep count 1 per lesson, the empty list). The live run verify_refs.py --unit E4 needs the network and was not run.")

# ---------------- hours and numbers (exact re-derivation) ----------------
row("E4a-hours", "2.9-structure", "index.html lines 29, 40-43; L01.html, L02.html, L03.html line 2", "PASS",
    "index data-hours-lessons=72, data-hours-project=28, hours-split bars 72%/28%; lessons data-hours=8 on L01, L02, L03; 9 x 8 = 72, 72 + 28 = 100, 28% of 100 = 28 (ledgers/E4/scripts/E4-a-r3/rederive_numbers.py 'hub' checks, logs/rederive_numbers.txt).")
row("E4a-num-hub", "2.2-numbers", "index.html lines 68, 113-120", "PASS",
    f"{S}/rederive_numbers.py (exact Fractions, 98 checks, 98 OK, {L}/rederive_numbers.txt): 7 of 8 = 87.5%, 6 of 8 = 75%; item 1 expectation 6; item 2 derivative 1/4; item 5 expected utility 8; item 7 value 25/2 = 12.5; item 8 demand 4.")
row("E4a-num-L01", "2.2-numbers", "L01.html lines 92-93, 113-161, 262-281, 320-336, 345-347, 386, 402-404, 447-463, 484-486", "PASS",
    f"{S}/rederive_numbers.py L01 block: V(claim)=340/3, V(other)=56, combination (200,50,-60,485) with V=596/3 on both sides, E claim = 235/4 = 58.75, V(claim) = 113.33 to 2 dp, V - E = 655/12; M1 V = 55/3 (18.33 to 2 dp), E = 25/2, gap 35/6; M2 25; M3 comb (-5,6,7), V = -1/8, V(x)=11/8, V(y)=17/8; R2 V(e1)=1/4, V(2e1)=1; quiz 4.25, 3, 0.6.")
row("E4a-num-L02", "2.2-numbers", "L02.html lines 187, 192, 299-337, 338, 355-363, 377-393, 429-443, 506-530", "PASS",
    f"{S}/rederive_numbers.py L02 block: aggregate (4,8,4); theta1=9/16, theta2=7/16; q*=(1/8,1/32,1/16), q*.ebar=1; x1*=(9/4,9/2,9/4), x2*=(7/4,7/2,7/4); budgets bind (w1=q*.e1=9/16, w2=7/16); clearing; ratios pi/(x q)=16/9 and 16/7 = 1/w; Part E wealth 27/16 and x unchanged at 3q; wealth fixed falls by factor 3; M1 (1,2); M2 (3/4,3/8,3/2) spend 3; M3 q*=(1/8,1/8), theta=1/2; MC2 q.z=3/32; quiz q*_1=0.125 and q*_3=0.0625.")
row("E4a-num-L03", "2.2-numbers", "L03.html lines 119, 124, 250-261, 301-310, 335-336, 353, 385, 406, 476", "PASS",
    f"{S}/rederive_numbers.py L03 block: MRS agent 1 and agent 2 = 4, 2, 1/2 (equal to q*_1/q*_2=4, q*_1/q*_3=2, q*_2/q*_3=1/2); Example 3.6 endowment MRS 8/3 (agent 1) and 8 (agent 2); M1 MRS 2; M2 MRS 2; P2 identity; R2 derivatives 1/12 and 1/4 and feasibility of the trade; grid 125, 0 improvements at equilibrium, 2 at endowment, first witness ((2,4,3),(2,4,1)) reproduced from the twin's own grid logic.")

# ---------------- math (proofs) ----------------
row("E4a-math-L01", "2.4-mathematics", "L01.html lines 77-151, 286-287, 358-361, 393-412", "PASS",
    "Prop 1.4 (single nonzero term; finite by A1), Prop 1.7 (induction on finite sums from A2; finiteness from A1), Prop 1.8 (take x = e_s), Prop 1.10 both directions (E e_s = pi_s; V(x)=E x under (b)), P2 (a=0,b=0; a=-1,b=0), P3 (contrapositive of Prop 1.10, not a converse counterexample), R2 counterexample V(2e1)=1 vs 2V(e1)=1/2, R3 both directions. Hypotheses cited by number (A1, A2). Canon-breaks at line 287 says the countable step is 'not justified without an extra condition' and that the lesson does not verify one; R1 solution (line 397) gives continuity along partial sums as an example of such a condition, which is a valid sufficient condition given convergence. Noted, not a FAIL.")
row("E4a-math-L02", "2.4-mathematics", "L02.html lines 99-178, 111-116, 128-136, 451-455", "FAIL",
    "Lemma 2.4 (z = w/(2 q.iota) iota, finite utility, A4), Prop 2.5 proof (tangent of budget, A1 for strict increase, Lemma 2.4 applies because w_i = q.e^i > 0), Prop 2.8 (tangent-line inequality for ln, pi_s/x*_s = q_s/w, equality case), Prop 2.9 (theta sums to 1, q*.ebar=1, x*=theta ebar, clearing) all re-derived and correct. The defect is the hypothesis of Corollary 2.7 (line 130), which uses z(q) with no demand hypothesis. Under A4 alone a demand need not exist (see E4a-r3-walras-demand-existence, witness ledgers/E4/scripts/E4-a-r3/no_demand_witness.py).",
    "Corollary 2.7 (L02.html line 130): add 'and let x^1, x^2 be demands at q (so that z(q) is defined)'. The proof then cites Proposition 2.5 correctly. See E4a-r3-walras-demand-existence.")
row("E4a-math-L03", "2.4-mathematics", "L03.html lines 81-110", "PASS",
    "Proof of (a): Steps 1-3 re-derived line by line (Step 1: q.y^i > w_i if U_i(y^i) > U_i(x^{i*}), by the demand property; Step 2: q.y^i >= w_i by A4 strict monotonicity and A1; Step 3: adding gives q.(y^1+y^2) > q.ebar, contradicting feasibility). Proof of (b): the bundle change d has q*.d = 0; G = pi_s u'(x_s)/q_s - pi_t u'(x_t)/q_t; G = 0 by the demand property; u'(x_t) > 0 from monotone and concave u_i (line 109). Hypotheses A1, A3, A4 stated in the proposition. The M2 and Remark 3.5 defects are separate rows.")
row("E4a-math-L03-b-uprime", "2.4-mathematics", "L03.html line 109 (proof of (b)), line 69 (Def 3.3)", "PASS",
    "Round-2 FAIL fixed. Line 109 now reads: u_i' is nonnegative because u_i is strictly increasing and nonincreasing because u_i is concave; if u_i'(x_t)=0 then 0 <= u_i'(y) <= 0 for every y > x_t, so u_i is constant on (x_t, inf), contradicting strict monotonicity; hence pi_t u_i'(x_t)/q*_t > 0 before dividing G = 0. Re-derived: correct. Definition 3.3 (line 69) now says u_i' is positive as shown in the proof of (b).")

# ---------------- assumptions and scope ----------------
row("E4a-assumptions", "2.4-mathematics", "L01.html lines 61, 99; L02.html lines 58, 63, 93; L03.html line 55", "PASS",
    "A1 (L01 line 61), A2 (L01 line 99), A3 (L02 line 58), A4 (L02 line 63), A5 (L02 line 93) numbered and stated before use; L03 line 55 lists A1, A3 and A4 and Prop 3.4 (line 82) assumes A1, A3, A4 plus an equilibrium; every Proposition cites its Assumptions by number.")
row("E4a-existence-scope", "2.4-mathematics", "L02.html lines 51, 94, 182, 345; L03.html line 268", "PASS",
    "A5 (L02 line 94) is a hypothesis, not proved; L02 line 345 and L03 line 268 name A5 as the hypothesis; Remark 2.10 (line 182) says Prop 2.9 does not prove uniqueness. Existence of demands under A4 is a separate issue, raised in E4a-r3-walras-demand-existence.")
row("E4a-A2-nonlinear-sources", "2.9-prose", "L01.html line 104", "PASS",
    "'A2 excludes quantity discounts, bid-ask spreads and price impact, because each of those makes V nonlinear': conceptual; a quantity discount gives V(2x) != 2V(x) (R2, line 404 gives the size case); the sentence adds that A2 is an assumption the lesson does not derive (line 104).")
row("E4a-scope-words", "2.9-prose", "L02.html line 182 (Remark 2.10); also L01.html line 511", "FAIL",
    "Scope words (every, all, any, always, never, only, same, exactly, drives, in general): 226 whole-word hits across index, L01-L03 (grep -oiwE, this round); each read in its sentence while reading every sentence of the slice. Two sentences fail. (1) L02 line 182, Remark 2.10: 'Demand depends on the price and wealth only through x_s = pi_s w / q_s.' The formula is the logarithmic demand of Prop 2.8, and line 346 says that for other A4 utilities it 'need not give the demand'; the 'only' is stated without its log hypothesis. (2) L01 line 511 (references, row E4a-r3-L01-references-labs): 'the labs compute the numbers it quotes' is wider than the labs, which print only 340/3, 56, 596/3, 235/4.",
    "L02 line 182: begin with 'Under logarithmic utility, demand depends on the price and wealth only through ...'. L01 line 511: see E4a-r3-L01-references-labs. Other scope words in the four pages are backed by a derivation, a finite check labelled C, or a stated hypothesis.")
row("E4a-r3-walras-demand-existence", "2.4-mathematics / rule 6 (hypotheses)", "L02.html line 51 (why-it-matters), line 130 (Corollary 2.7), line 510 (quiz Q3)", "FAIL",
    "Prop 2.5 (L02 lines 111-112) is stated 'let x^1 and x^2 be demands at q'. Three summaries drop that hypothesis. Line 51: 'the value of the excess demand is zero at any positive price vector'. Line 130: Corollary 2.7 assumes only A1, A3, A4 and q in (0, inf)^S. Line 510: Q3 asks about 'any prices q with q >= 0'. Under A4 alone a demand need not exist: witness ledgers/E4/scripts/E4-a-r3/no_demand_witness.py (log in logs/no_demand_witness.txt): u(x)=1-exp(-x) is strictly increasing, strictly concave and differentiable on (0, inf); pi=(0.1,0.9), w=1, q=(1,25). The interior sup of U along the budget line is approached as x_2 -> 0+ (numerical slope -0.0197 at the corner), and the boundary bundle (1,0) has U = -inf, so no bundle maximises U on B(q). Definition 2.3 defines z(q) only from chosen demands, so z(q) is undefined there. The lesson does not establish demand existence under A4.",
    "Line 51: replace 'at any positive price vector' with 'at any positive price vector at which each agent has a demand'. Line 130: add 'and let x^1, x^2 be demands at q'. Line 510 (Q3): 'which identity holds at any prices q with q >= 0 at which both agents have demands?' Optionally add one sentence in section 2 that demand existence is a hypothesis under A4 (the witness shows it can fail).")
row("E4a-r3-remark26-witness", "2.2-numbers / 2.9-prose (need claims)", "L02.html lines 124-126 (Remark 2.6)", "FAIL",
    "Remark 2.6 says 'The unweighted excess demands need not add to zero' and points to Misconception 2. Misconception 2 (line 360) shows a different fact: the zero-sum vector (1,-1,0) is not an excess demand at q*, since q.z = 3/32. No witness of a nonzero unweighted sum appears on the page. Witness computed (ledgers/E4/scripts/E4-a-r3/remark26_witness.py, log logs/remark26_witness.txt): in the Example 2.11 economy at q = (2,1,1), w_1 = 11, w_2 = 9, z(q) = (1,-3,1), unweighted sum -1, weighted q.z = 0 (Prop 2.5 holds). The claim is true; it is unsupported on the page.",
    "After line 125 add: 'At q = (2, 1, 1) the excess demand of Example 2.11 is (1, -3, 1): its unweighted sum is -1, while q . z = 0.'")
row("E4a-r3-remark210-title", "2.2-lab-statements / 2.9-prose", "L02.html line 181 (Remark 2.10 title); tests/labs/E4/lab-E4-L02-1.py lines 16-17 (page lines 208-209)", "FAIL",
    "The Remark title '(the price is fixed only up to scale)' and the Part E docstring 'so the prices are fixed only up to scale' assert that equilibrium prices are determined up to scale. The Remark body says 'Proposition 2.9 does not prove that q* is the only equilibrium price vector', and Part E prints only demand_unchanged True for both agents (L02.html lines 334-335), which tests no uniqueness. The body supports only that demand does not fix the scale of q.",
    "Retitle Remark 2.10 '(the scale of the price is not fixed by demand)'. In the twin lines 16-17 replace 'so the prices are fixed only up to scale' with 'so demand does not fix the scale of the prices', then re-embed: tools/embed_labs.py course/modules/E/E4/L02.html --refresh lab-E4-L02-1.")
row("E4a-r3-remark35-hypotheses", "2.9-prose / rule 6 (hypotheses list)", "L03.html line 114 (Remark 3.5), line 342 (P3 solution), line 448 (quiz Q4 explanation)", "FAIL",
    "Remark 3.5 says part (b) 'uses the differentiability in A4 and the strict positivity of the equilibrium bundle' and nothing else. The proof of (b) also uses the strict monotonicity and the concavity of u_i, which show u_i' > 0 (L03 line 109: 'u_i' is nonnegative because u_i is strictly increasing, and nonincreasing because u_i is concave'). Without them the denominator of MRS is not shown nonzero. P3's solution (line 342) repeats the incomplete list, and Q4 says 'Remark 3.5 lists the hypotheses of each part'.",
    "Remark 3.5 (line 114) and P3 solution (line 342): add 'and the strict monotonicity and concavity of A4, which show that u_i' is positive (proof of (b))'.")
row("E4a-L03-M2-scope", "2.9-prose", "L03.html line 310 (M2 solution)", "FAIL",
    "Round-2 row, text changed, so re-verified. The M2 solution reads: 'The proof of Proposition 3.4 (b) derives this equality for a strictly positive demand at prices q, since it uses only the demand property and the budget.' The (b) proof (L03 lines 105-109) also uses the differentiability of u_i (A4), the derivative u_i' in G, and the positivity of u_i' from strict monotonicity and concavity. 'Only the demand property and the budget' is false.",
    "Replace with: 'The proof of Proposition 3.4 (b) derives this equality for a strictly positive demand at prices q. It uses the demand property, the budget, and the differentiability of A4, together with u_i' > 0 from strict monotonicity and concavity.'")

# ---------------- structure, hub, prose ----------------
row("E4a-struct-hub", "2.9-structure", "index.html lines 66-123 (placement); lines 35, 63 (prerequisites)", "FAIL",
    "Objectives 8 with measurable verbs (lines 49-58); prerequisites E2, E3, M7 (line 35) match curriculum.json; lesson map of 9 cards (lines 128-138); ladder with 4 rungs (lines 144-149); data status (lines 153-156); data-mastery 0.8 and 7-of-8 arithmetic (line 68). Defect: BUILDER_RULES 5.1 says the non-skill placement items 'test the prerequisites, including every prerequisite module'. E2 is a direct prerequisite (line 35, 63), but none of the six prerequisite items (lines 70-110) tests an E2 concept: they test M4 expectation, M2 derivative, M7 Lagrange, E1 competitive equilibrium, E3 expected utility and M3 linear maps (verified by grep: 0 placement lines mention E2, adverse selection, game theory or Bayesian).",
    "Replace one of the six prerequisite items with an E2 item (for example a question on a concept E2 introduces, such as adverse selection or the Bayesian-Nash equilibrium), keeping six prerequisite items and two skill items, and keep the 7-of-8 bar arithmetic.")
row("E4a-r3-placement-skill-items", "2.9-structure (BUILDER_RULES 5.1)", "index.html lines 112-120 (data-skill items 7 and 8); project.html lab-E4-project-2; index.html lines 145-146", "FAIL",
    "Item 7 (line 113), labelled 'Skill check (rung 1)', asks for the value of a claim under Arrow-Debreu prices (Lesson 1, Prop 1.7). The project's rung 1 is 'a fully solved and annotated run of the solver' (index line 145; project.html Rung 1), which involves the informed-fraction equation, bracket, bisection, indifference gap and informativeness, not claim valuation. Item 8 (line 118), labelled 'Skill check (rung 2)', asks for a logarithmic demand, while the project's rung 2 blanks the return of indifference_gap (project.html 'Lab 2 · Completion problem': 'Replace the ___ with the expression that completes the return of indifference_gap: the uninformed term F_U minus e^{ac} times the informed term F_I'). Neither item tests a skill rungs 1-2 teach. BUILDER_RULES 5.1 requires that 'at least two items test the skills rungs 1-2 teach'.",
    "Rewrite items 7 and 8 as questions on the skills the project's rungs 1 and 2 teach: the bisection bracket and sign-change step for the informed fraction, and the indifference-gap expression F_U - e^{ac} F_I at a stated fraction. Keep the explanations consistent with project.html.")
row("E4a-hub-placement-explain", "2.9-prose", "index.html lines 78, 87, 96, 101, 110, 115, 120", "FAIL",
    "Items 1-6 explanations re-read against their lessons and correct (line 78 uses Lesson 2's first-order condition, which L02 Lab 2 Part D names 'first-order ratio'; line 96 cites Definition 2.2; line 110 cites M3; line 120 cites Prop 2.8). Defect at line 120: 'Rung 2 asks you to fill in the step that divides by the price.' The rung 2 blank in project.html is the return of indifference_gap (F_U minus e^{ac} F_I), not a division by a price, so the sentence misdescribes rung 2.",
    "Replace the final sentence of line 120 with a description of the rung 2 blank that matches project.html, for example: 'Rung 2 asks you to complete the indifference-gap return, the step that compares the two expected utilities.' (Pair with the item rewrite in E4a-r3-placement-skill-items.)")
row("E4a-r3-hub-CU", "2.9-prose / defined terms (plan 2.1 item 8)", "index.html lines 71, 73 (placement item 1)", "FAIL",
    "Item 1 prompt: 'A lottery pays 0 CU with probability 1/4 and 8 CU with probability 3/4. What is its expected value, in CU?' Explanation (line 73): '= 6 CU'. 'CU' is defined nowhere in E4: grep -n CU across index, L01-L03 and the twins returns only lines 71 and 73. L01 states payoffs in cents (Definition 1.2, line 67: 'in cents'; Example 1.5). Plan 2.1 item 8 says any currency unit must be integer cents.",
    "Replace 'CU' with 'cents' in line 71 (payoffs 0 and 8 cents, expected value in cents) and in line 73 ('= 6 cents').")
row("E4a-quiz-items", "2.9-prose", "L01.html lines 437-505; L02.html lines 495-567; L03.html lines 418-486", "FAIL",
    "27 quiz items re-read; keys recomputed. L01 9 items OK (L01q1 coefficient 7; Q2 4.25; Q3 2V(x); Q4 expected 3; Q6 A1; Q7 0.6; Q8 r=q; Q9 size discount). L03 9 items OK (MRS 2, Q6 explanation 'two different bundles can share a rate', Q8 MRS 4, Q9 Step 2). L02 Q3 (line 510): 'Walras' law for two agents says which identity holds at any prices q with q >= 0?' has the defect in E4a-r3-walras-demand-existence (it omits the demand hypothesis); the other eight L02 items are correct.",
    "Q3 (L02.html line 510): add 'at which both agents have demands' to the prompt. See E4a-r3-walras-demand-existence.")
row("E4a-r3-L01-references-labs", "2.9-prose / rule 4 (scope)", "L01.html line 511 (section 9 References)", "FAIL",
    "'Each graded result in the table of §7 is proved on this page (grade T) from Definitions 1.1 to 1.9 and the assumptions A1 and A2, and the labs compute the numbers it quotes.' The labs print 340/3, 56, 596/3 and 235/4 only. The page also quotes 12.5 and 18.33 and 35/6 (M1, line 322), 58.75 and 113.33 (E3, line 386), 4.25 (quiz line 449) and 0.6 (quiz line 486), which no lab prints; they are exact hand computations on the page.",
    "Replace 'and the labs compute the numbers it quotes' with 'and Lab 1, Parts B to D, reproduces its exact values 340/3, 56, 596/3 and 235/4'.")
row("E4a-banned-phrases", "2.9-prose", "index.html, L01.html, L02.html, L03.html", "PASS",
    "check_pages.py banned-string check PASS on all four pages (re-run). Grep for TODO, TBD, lorem, 'for brevity', 'beyond the scope', 'it is important to note', 'obviously', 'clearly', 'studies show', 'well known', 'experts agree', 'left as an exercise', 'details omitted': no hits. '...' appears only inside Python code (L01 line 181; L02 code; L03 code), where it is a type ellipsis.")
row("E4a-process-words", "2.9-prose", "index.html, L01.html to L03.html, lab-E4-L01-1 to L03-1", "PASS",
    "Grep for build, builder, round, verifier, REQUEST, planner, architect, fixer, ruling, plan, unit report, ledger: hits only 'rounding' (L02.html line 198; twin L02 line 6), an ordinary word.")
row("E4a-struct-lessons", "2.9-structure", "L01.html, L02.html, L03.html", "PASS",
    "why-it-matters 105 (L01), 112 (L02), 120 (L03) words, each at most 120 (counted from the HTML). Numbered core sections; inline lab before 'Where the canon breaks'; canon-breaks section; 3 misconceptions each; Mechanics, Proof, Empirical and Research tiers with 3 problems each (12 details.solution blocks, each over 15 words); key-results table; 9 quiz items each; references section with empty data-references; lesson-nav.")
row("E4a-hub-cards-h1", "2.9-structure", "index.html lines 129-137; L01-L03 <h1> (lines 35)", "PASS",
    "Card titles equal the <h1> exactly: L01 'Arrow–Debreu securities and state-contingent payoffs', L02 'Arrow–Debreu equilibrium', L03 'The first welfare theorem' (L01.html 35, L02.html 35, L03.html 35, re-read this round).")
row("E4a-hub-cards-h1-L04-L05", "2.9-structure", "index.html lines 132-133; L04.html and L05.html <h1>", "PASS",
    "Round-2 FAIL fixed. Card L04 'Complete and Incomplete Markets' equals L04.html <h1> 'Complete and Incomplete Markets'; card L05 'Rational-Expectations Equilibrium' equals L05.html <h1> 'Rational-Expectations Equilibrium' (grep <h1> of L04-L09 this round). L06-L09 cards equal their h1 too.")
row("E4a-hub-prereq-unlock", "2.9-structure", "index.html lines 35-36, 63", "PASS",
    "curriculum.json records (re-read this round): E4 prereqs ['E2','E3','M7'], hours 100, tier M. Titles: E1 'Microeconomics', E2 'Game Theory & Information Economics', E3 'Decision Theory Under Risk & Ambiguity', M7 'Optimization', AP1 'No-Arbitrage & the Stochastic Discount Factor', AP6 'Intermediary & Institutional Asset Pricing', MS1 'Microstructure Theory', SR1 'Runs, Liquidity & Fire Sales'. Modules listing E4 as a prerequisite: AP1, AP6, MS1, SR1 (the hub's unlock list is exact). Hub concept links: E1 introduces utility-maximization, competitive-equilibrium, pareto-efficiency, externality; E3 expected-utility, certainty-equivalent, arrow-pratt-risk-aversion; E2 adverse-selection; M7 lagrange-multiplier, kkt-conditions; M4 random-variable, expectation, variance, correlation, normal-distribution, conditional-expectation-elementary; M3 linear-map, vector-space, orthogonal-projection; M2 derivative, gradient.")
row("E4a-hub-introduces", "2.5-DAG", "L01.html line 38, 74; L02.html line 38, 89; L03.html line 38, 78", "PASS",
    "Each lesson's 'Introduces' names its one concept (arrow-debreu-security, arrow-debreu-equilibrium, first-welfare-theorem), and each has exactly one <dfn data-concept> in its lesson (L01 line 74, L02 line 89, L03 line 78). curriculum.json E4 introduces nine concepts including these three.")
row("E4a-dag-outside-closure", "2.9-DAG", "index.html, L01.html, L02.html, L03.html", "PASS",
    "Plain-text grep for bayes, posterior, state price, stochastic discount, martingale, efficient market, informationally efficient, CARA, common knowledge, two-fund, diagnostic, intermediate value, banach, Muth, Milgrom, Mas-Colell: no lesson-text hit except the hub card of L09 ('posteriors as conditional probabilities', index line 137), plain prose with no link. 'noise traders' appears in the hub lede and card (lines 33, 127, 134) as a preview; it is defined in L06 (outside this slice). 'fixed point' (index lines 54, 133) is generic, not a named theorem.")
row("E4a-links-earlier-lessons", "2.9-DAG", "L02.html line 37, 84, 89; L03.html line 37, 64", "PASS",
    "L02 links L01.html#def-arrow-debreu-security (defined at L01.html line 74); L03 links L02.html#def-arrow-debreu-equilibrium (L02.html line 89) and L01.html#def-arrow-debreu-security. No link points to a later lesson. Prerequisite concept links use concepts.html anchors; check_dag PASS.")
row("E4a-define-before-use", "2.9-prose / defined terms", "L02.html line 51; L03.html line 51; body text of L01-L03", "PASS",
    "Round-2 FAILs fixed in running text: L02 line 51 no longer names Walras' law (defined at L02 line 110 in Proposition 2.5's title); L03 line 51 names 'the efficiency result proved below (Proposition 3.4)' and 'the rate ... (Definition 3.3)' with no undefined term. Grep: 'Walras' first occurs at L02 line 110 (the dfn inside Proposition 2.5's title) and line 7 (meta description, not body); 'marginal rate' first occurs at L03 line 53 (the section heading, see note) and then at line 68 (the Definition 3.3 dfn). NOTE (not counted as a FAIL): section headings name terms ahead of their definitions (L01 line 53 'claims', L02 line 53 'budgets and demand', L03 line 53 'Pareto improvements and marginal rates'); headings preview a section, so they are recorded here for the architect's ruling.")
row("E4a-define-interior", "2.9-prose", "L03.html line 51, 271, 310, 451", "PASS",
    "'interior' is defined with a plain <dfn> at its first use (L03 line 51) and used later only in the defined sense.")

# ---------------- lab statements and runtime ----------------
row("E4a-lab-hypothesis-before-output", "2.5-labs", "L01.html line 160 vs 262; L02.html line 192 vs 313; L03.html line 124 vs 250", "PASS",
    "Each hypothesis paragraph precedes its pre.expected block in page order (re-read).")
row("E4a-lab-L01-statements", "2.5-labs", "L01.html lines 160, 281; code lines 219-261 (twin lines 59-101)", "PASS",
    "Hypothesis numbers: coefficients 100, 40, 0, 250 (printed lines 263-266); value 340/3 (line 270); second claim 56; combination weights 2 and -1/2, equal True (line 273); expected payoff 235/4 (line 275); value 340/3 with flag False (line 277); two rejections (negative entry; sum 9/8 from 1/8+3/8+3/8+1/4, printed lines 279-280). Interpretation (line 281) matches. Misconception 3 claim (check at start of main(), code line 222) matches.")
row("E4a-lab-L02-statements", "2.5-labs", "L02.html lines 192, 193-212, 338; tests/labs/E4/lab-E4-L02-1.py", "PASS",
    "Hypothesis (aggregate (4,8,4); shares 9/16, 7/16; prices; demands; ratio 16/9 and 16/7 equal to one over wealth; Part E with re-valued wealth; Part F zero endowment rejected) matches printed lines 314-337. Interpretation: five residuals and Walras residual 0 (lines 323-329). Docstring lines 193-212 match the code.")
row("E4a-lab-L03-interpretation", "2.5-labs", "L03.html lines 124, 261; tests/labs/E4/lab-E4-L03-1.py lines 1-20", "PASS",
    "Hypothesis: MRS 4, 2, 1/2 equal price ratios (printed lines 252-254); grid of 125 with {0,1/4,1/2,3/4,1}; zero improvements at equilibrium and at least one at endowment (printed lines 258-259); TOL 1e-12 (twin line 159). Interpretation: 0 of 125 and 2 of 125; first witness (2,4,3)/(2,4,1) (line 260). Twin docstring line 139-140 (worse when below by more than TOL) matches improves() (twin lines 194-198).")
row("E4a-lab-runtime-rng-stdlib", "2.5-labs", "tests/labs/E4/lab-E4-L01-1.py, L02-1.py, L03-1.py", "PASS",
    "Imports: __future__, fractions (L01, L02); math, fractions, itertools (L03). No random import and no draw in any twin (grep 'random' returns nothing). Each twin's last line is an unconditional main() call (lab-E4-L01-1.py:101, lab-E4-L02-1.py:120, lab-E4-L03-1.py:125), with no __name__ guard. page_smoke lab times 0.0 s each (under 10 s).")
row("E4a-simulated-data", "2.8-data", "index.html lines 38, 155; L01-L03 labs", "PASS",
    "No data-files attribute in the slice and no dataset is named. Every lab is exact arithmetic on fixed inputs, with no random draws, so no SIMULATED label is needed in this slice; the hub says no data is used (line 155).")
row("E4a-figures", "2.8-figures", "index.html, L01.html, L02.html, L03.html", "PASS",
    "grep -c for svg, <figure, data-figures in the four pages: 0 each.")
row("E4a-mutants", "2.6-grader", "tests/labs/E4 (no grader in slice a)", "PASS",
    "The slice has no grader. Lab twins are demonstrations; mutation testing applies to project graders only (LAB MUTANTS ruling). No mutant is claimed for slice a.")

# ---------------- L01 round-2 fixes, re-read ----------------
row("E4a-L01-misc2-partA", "2.9-prose", "L01.html line 307; code line 222 (twin line 62)", "PASS",
    "Round-2 FAIL fixed. Misconception 3: 'Lab 1 checks its unequal probabilities once, at the start of main(), before Part A.' Code line 222 calls check_probabilities(STATE_PROBABILITIES) before the Part A print (code line 224). Correct.")
row("E4a-term-additive", "2.9-prose", "index.html lines 50, 129; L01.html lines 7, 51", "PASS",
    "Round-2 FAIL fixed. 'additive' does not appear in the four pages (grep); the text now says 'linear valuation of A2', which is the property the lesson assumes (A2, L01 line 99).")
row("E4a-L01-R2-title", "2.9-prose", "L01.html line 401 (title), lines 402-404 (solution)", "PASS",
    "Round-2 FAIL fixed. Title 'A size effect breaks linearity'; V(x) = (sum q_s x_s)^2 gives V(2e1) = 1 = 4 V(e1), a size effect, consistent with the canon-breaks text (line 288).")
row("E4a-L01-continuity-necessity", "2.9-prose", "L01.html line 287 (canon-breaks), line 397 (R1 solution)", "PASS",
    "Round-2 FAIL reworded. Line 287 says the step is 'not justified without an extra condition on V' and that the lesson does not verify a sufficient condition; line 397 offers continuity along partial sums as one example. Neither line asserts the formula is false without the condition. Note (not a FAIL): R1 offers an example condition while line 287 says the lesson does not state one; the example is 'for example', so the wording is accepted.")
row("E4a-L01-P3-title", "2.4-mathematics", "L01.html line 358 (title), lines 359-361 (solution)", "PASS",
    "Round-2 FAIL fixed. Title 'Prices that differ from probabilities, two states'; solution line 361 says it is the contrapositive of Proposition 1.10 and 'not a counterexample to a converse'. Re-derived: V(e1) = 1/4 != 1/3 = E e1.")

# ---------------- L02 round-2 fixes, re-read ----------------
row("E4a-L02-residual-count", "2.5-labs", "L02.html line 338; expected block lines 322-329", "PASS",
    "Round-2 FAIL fixed. Interpretation: 'five budget and market-clearing residuals (two budget, three market-clearing) and the Walras residual are 0 exactly'. Printed lines 323, 325 (two budget_residual), 326-328 (three market_clearing_residual), 329 (walras_law_residual 0).")
row("E4a-L02-partE-wealth", "2.2-numbers / 2.5-labs", "L02.html lines 182, 192, 208, 298-302, 338, 443; twin docstring lines 16-17", "PASS",
    "Round-2 FAIL fixed. Each unchanged-demand statement re-values wealth at the new prices (lines 192, 208, 338, 443). Re-derivation: with wealth fixed the demand falls by 3 (rederive_numbers.py L02 block). The Part E docstring's scale claim is a separate row (E4a-r3-remark210-title).")
row("E4a-L02-partF-docstring", "2.5-labs", "tests/labs/E4/lab-E4-L02-1.py docstring line 18; L02.html lines 210, 337", "PASS",
    "Round-2 FAIL fixed. Part F input contains Fraction(0) and check_economy raises ValueError for entries <= 0; message at printed line 337 matches. Docstring and page agree.")
row("E4a-L02-uniqueness-z", "2.9-prose", "L02.html lines 84, 89, 148", "PASS",
    "Round-2 FAIL reworded. Definition 2.2 defines a demand as a maximiser in the budget set; Definition 2.3 says x^i(q) denotes 'the demand chosen for agent i at q' and z(q) is computed from those choices. Uniqueness is proved only for the logarithmic case (Prop 2.8, line 148). The defined z(q) presupposes chosen demands; the hypothesis gap in the summaries is a separate row (E4a-r3-walras-demand-existence).")
row("E4a-L02-CRRA-no-closed-form", "2.4-mathematics", "L02.html line 346 (canon-breaks)", "PASS",
    "Round-2 FAIL fixed. Now: 'the utility -1/x on (0, inf) satisfies A4, and this lesson does not derive its demand'. Checked: u' = 1/x^2 > 0, u'' = -2/x^3 < 0, differentiable on (0, inf).")
row("E4a-L02-A4-finite-zero", "2.4-mathematics", "L02.html line 68", "PASS",
    "Round-2 FAIL fixed. 'The display in A4 sets U_i = -inf at a zero entry, so the value of u_i at zero never enters; no result below uses it.' Consistent with Lemma 2.4 and Prop 2.5.")
row("E4a-wi-positive", "2.4-mathematics", "L02.html line 120 (proof of Prop 2.5); L03.html line 93 (proof of Prop 3.4 (a))", "PASS",
    "Round-2 FAIL fixed. Both proofs now state 'w_i = q.e^i > 0, because q is strictly positive and e^i is strictly positive by A3' before invoking Lemma 2.4 (L02 line 119; L03 line 93).")

# ---------------- L03 round-2 fixes, re-read ----------------
row("E4a-L03-remark36", "2.9-prose", "L03.html line 59 (Definition 3.1); research problem R1 at line 375-378", "PASS",
    "Round-2 FAIL fixed. Definition 3.1 says 'Research problem R1 treats the case with free disposal'; R1 (line 375-378) does, and its solution re-derives. No 'Remark 3.6' is referenced.")
row("E4a-L03-state-labels", "2.9-prose / notation", "L03.html line 406 (key-results row); lines 119, 302, 384, 473; L02.html line 355", "PASS",
    "Round-2 FAIL fixed. Key-results row now reads 'MRS_12 = 4, MRS_13 = 2, MRS_23 = 1/2', matching Example 3.6 (line 119) and Lab 3 output (lines 252-254, states 1-indexed).")
row("E4a-L03-R3-cannot", "2.9-prose", "L03.html lines 389-393", "PASS",
    "Round-2 FAIL fixed. The R3 solution explains that a move lowering a zero entry leaves the orthant and the utility is -inf there. Re-read: correct and consistent with Remark 3.5 (line 114).")
row("E4a-L03-lab3-because", "2.5-labs", "L03.html line 124", "PASS",
    "Round-2 FAIL fixed. 'The lesson gives no proof of this prediction, and the printed count is the evidence.' No unsupported 'because'.")

# ---------------- notation and attribution ----------------
row("E4a-notation-mathbf1", "2.4-notation", "index.html; L01.html lines 345-347, 486; L02.html lines 106, 120, 525; L03.html line 95; twins", "PASS",
    "Round-2 FAIL fixed. grep -cF '\\mathbf' is 0 in all four pages and the three twins. The vector of ones is \\iota (L01 line 345, L02 line 106, L03 line 95).")
row("E4a-notation-registered", "2.4-notation", "index.html, L01.html, L02.html, L03.html", "PASS",
    "Registered macros only: \\R (index 1, L01 3, L02 3, L03 1 uses) and \\E (L01 8 uses); grep -cF: no \\mathbb, \\Phi, \\gamma, \\ast, \\Corr, \\Var, \\Cov, \\Normal, \\argmax, \\indic, \\lambda in the slice; T is not used as a count. Symbols zeta (hub multiplier), psi (L02 scale) and iota (vector of ones) are unregistered local symbols, each used with one meaning.")
row("E4a-notation-lambda", "2.4-notation", "index.html lines 81, 83, 84; L02.html lines 182, 409-411, 542-548", "PASS",
    "Round-2 FAIL fixed. The hub multiplier is now zeta (lines 81, 83, 84); the scale factor is psi in L02 (Remark 2.10, P2, Q7). grep -cF '\\lambda' is 0 in the slice, so lambda is reserved for the informed fraction in L08 (outside this slice).")
row("E4a-notation-gamma", "2.4-notation", "L02.html line 346", "PASS",
    "Round-2 FAIL fixed. The power-utility example is replaced by -1/x; grep -cF '\\gamma' is 0 in the slice.")
row("E4a-attribution", "2.1-citations / attribution", "index.html, L01.html, L02.html, L03.html", "PASS",
    "No data-cite attribute; data-references lists empty; no author names, years or bibliographic data. 'Grossman–Stiglitz' appears only as the paradox's name (index lines 7, 33, 56, 136), with no paper attributed. Walras' law is an eponym, not a citation. Muth, Milgrom, Mas-Colell and Stiglitz do not appear in the slice.")

# ---------------- verifier metadata ----------------
notes = [
    "Slice: course/modules/E/E4/index.html (hub, 161 lines), L01.html (524 lines), L02.html (586 lines), L03.html (505 lines) and twins tests/labs/E4/lab-E4-L01-1.py, lab-E4-L02-1.py, lab-E4-L03-1.py (101, 120, 125 lines). Every line read in this round. The delta since the round-2 pin 67c47689 is 29 changed lines in the four pages; the three twins are byte-identical to that pin (git diff empty).",
    "Round-2 fragment (/Users/billyribeiro/.fanout/frags/E-E4-a.round2.json) was context only. Every round-2 row id is kept. Rows whose subject changed were re-verified from the text; rows whose subject is unchanged were re-run or re-read this round.",
    "Round-2 FAILs now fixed and PASS: E4a-math-L03-b-uprime, E4a-L03-state-labels, E4a-L01-P3-title, E4a-wi-positive, E4a-notation-lambda, E4a-notation-gamma, E4a-hub-cards-h1-L04-L05, E4a-define-before-use (running text), E4a-L02-residual-count, E4a-L02-partE-wealth, E4a-L02-partF-docstring, E4a-L02-uniqueness-z, E4a-L02-CRRA-no-closed-form, E4a-L02-A4-finite-zero, E4a-L03-remark36, E4a-L03-R3-cannot, E4a-L03-lab3-because, E4a-L01-misc2-partA, E4a-term-additive, E4a-L01-R2-title, E4a-L01-continuity-necessity, E4a-notation-mathbf1.",
    "Round-2 FAIL still open or newly open: E4a-L03-M2-scope (text changed; now a different false sentence), E4a-hub-placement-explain (item 8 explanation, found this round), E4a-struct-hub (E2 not tested by placement, found this round), E4a-scope-words (Remark 2.10 'only through', L01 references overclaim), E4a-math-L02 and E4a-quiz-items (cross-reference to E4a-r3-walras-demand-existence).",
    "Notation note for other slices (not a FAIL here): plan 2.3 lists s as the signal, but s is the state index throughout L01-L03 (for example Definition 1.1 and Example 1.5). L06 and L07 must not use s for the signal. The pages use q for security prices where plan 2.3 lists p, so L06-L07 must use one price symbol consistently.",
    "Note (not counted): L03 section 1 heading names 'Pareto improvements and marginal rates' before Definitions 3.2 and 3.3; L01 and L02 headings name 'claims' and 'budgets and demand' before their definitions. Headings preview a section. Ruling requested from the architect.",
    "Note (not counted): L03 misconception 2 and quiz Q6 say equal rates at different bundles are possible; the page's reason is that the rate is a function of the bundle and two bundles can share a value. The misconception sentence reads 'because the rate depends on the bundle', which is incomplete but not false. In this example both equilibrium bundles are proportional to ebar, so the ratios x_s/x_t agree.",
    "Note (not counted): L02 Remark 2.10 and the Part E docstring are the subject of two rows (scope and title). Lab Part E prints demand_unchanged only; it does not test uniqueness.",
]

fragment = {
    "unit": "E4",
    "slice": "a",
    "round": 3,
    "verifier": "Haiku independent verifier, E4-a round 3 (did not build E4; no shared context with the builders)",
    "pin": "67a2d13e7575608e95b2e34a9c7c2a82c61b117b",
    "base": "67c47689c49435bc0e6639e3de4feded5eefdd64 (round-2 pin). Delta read hunk by hunk: L01 (2 hunks), L02 (6 hunks), L03 (7 hunks), index (2 hunks); the three twins are unchanged since the base.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE3-E4-a (detached at 67a2d13; .venv symlinked)",
    "scratch": "/tmp only for twin runs (cwd /tmp, python -I -W error, PATH only). Scripts and logs kept under ledgers/E4/scripts/E4-a-r3/ (check_twins_embed.py, rederive_numbers.py, no_demand_witness.py, remark26_witness.py, write_fragment.py, logs/).",
    "verified_at": "2026-11-04T10:34:23+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": notes,
    "summary": {},
}

statuses = [r["status"] for r in rows]
fragment["summary"] = {
    "rows": len(rows),
    "pass": statuses.count("PASS"),
    "fail": statuses.count("FAIL"),
    "unverifiable": statuses.count("UNVERIFIABLE"),
    "mutants_killed": 0,
    "mutants": 0,
}

out = ROOT / "ledgers" / "E4" / "E4-a.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out, fragment["summary"])
