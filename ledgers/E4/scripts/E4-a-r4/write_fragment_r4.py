"""Write the round-4 verifier fragment for E4 slice a (hub index.html, L01 to L03, twins L01 to L03).

Run from the checkout root: .venv/bin/python ledgers/E4/scripts/E4-a-r4/write_fragment_r4.py
Every PASS row names the command, script or log that backs it (paths under ledgers/E4/scripts/E4-a-r4/).
"""

from __future__ import annotations

import json
import pathlib
from datetime import UTC, datetime

ROOT = pathlib.Path(__file__).resolve().parents[4]
LOGS = "ledgers/E4/scripts/E4-a-r4/logs"
SCRIPTS = "ledgers/E4/scripts/E4-a-r4"

rows: list[dict[str, str]] = []


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str | None = None) -> None:
    item = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        if not fix:
            raise SystemExit(f"{rid}: non-PASS row needs a fix")
        item["fix"] = fix
    rows.append(item)


# ---- commands and tools (2.5, 2.9, 2.1) ----
row(
    "E4a-cmd-check_pages-unit",
    "2.9-structure",
    "index.html, L01.html, L02.html, L03.html",
    "PASS",
    f"tools/check_pages.py --unit E4 -> 'check_pages E4: PASS', exit 0; with --page L01/L02/L03 each PASS ({LOGS}/check_pages_unit.txt, check_pages_L01.txt, check_pages_L02.txt, check_pages_L03.txt).",
)
row(
    "E4a-cmd-check_pages-lessons",
    "2.9-structure",
    "L01.html, L02.html, L03.html",
    "PASS",
    f"Same run as E4a-cmd-check_pages-unit; per-lesson runs PASS ({LOGS}/check_pages_L0{{1,2,3}}.txt). Lesson 6 to 12 hour rule and 9-lesson hub split are enforced by the tool (tools/check_pages.py check_lesson, check_hub).",
)
row(
    "E4a-cmd-check_dag",
    "2.9-dag",
    "index.html, L01.html, L02.html, L03.html",
    "PASS",
    f"tools/check_dag.py --unit E4 -> 'check_dag E4: PASS', exit 0 ({LOGS}/check_dag.txt). Unlinked names of out-of-closure concepts checked by grep in E4a-dag-outside-closure.",
)
row(
    "E4a-cmd-run_labs",
    "2.5-labs",
    "tests/labs/E4/lab-E4-L01-1.py, lab-E4-L02-1.py, lab-E4-L03-1.py",
    "PASS",
    f"tools/run_labs.py --unit E4 -> 'run_labs E4: PASS (12/12)', exit 0; --page L01, L02, L03 each exit 0 ({LOGS}/run_labs_unit.txt, run_labs_L01.txt, run_labs_L02.txt, run_labs_L03.txt).",
)
row(
    "E4a-lab-twins-alone",
    "2.5-labs",
    "tests/labs/E4/lab-E4-L01-1.py, lab-E4-L02-1.py, lab-E4-L03-1.py",
    "PASS",
    f"Each twin run alone as `python -I -W error <twin>` from a temporary directory: exit 0, stderr empty, stdout recorded ({LOGS}/check_twins_embed.txt, lines 'twin exit 0; stderr empty: True' for L01, L02, L03).",
)
row(
    "E4a-lab-embed-equality",
    "2.5-labs",
    "L01.html, L02.html, L03.html (data-run and pre.expected blocks)",
    "PASS",
    f"{SCRIPTS}/check_twins_embed.py: the code in each page's <code data-run> equals the twin file (after trailing-whitespace strip), and each <pre class=expected> equals the twin's stdout. Output: 'embedded code == twin: True' and 'expected block == twin stdout: True' for L01, L02, L03 ({LOGS}/check_twins_embed.txt).",
)
row(
    "E4a-cmd-ruff",
    "2.5-labs",
    "tests/labs/E4/lab-E4-L01-1.py, lab-E4-L02-1.py, lab-E4-L03-1.py",
    "PASS",
    "`.venv/bin/python -m ruff check` on the three twins -> 'All checks passed!'; `ruff format --check` -> '3 files already formatted' (ruff 0.17.2).",
)
row(
    "E4a-cmd-mypy",
    "2.5-labs",
    "tests/labs/E4/lab-E4-L01-1.py, L02-1.py, L03-1.py",
    "PASS",
    f"`.venv/bin/python -m mypy --no-incremental` on the three twins -> 'Success: no issues found in 3 source files', exit 0 ({LOGS}/mypy_twins.txt).",
)
row(
    "E4a-cmd-page_smoke",
    "2.9-smoke",
    "index.html, L01.html, L02.html, L03.html",
    "PASS",
    f"tools/page_smoke.py --unit E4 --pages index L01 L02 L03 -> 'page_smoke modules/E/E4/{{index,L01,L02,L03}}.html: PASS' and 'page_smoke E4: PASS', exit 0; lab runs 0.0 s each ({LOGS}/page_smoke_slice.txt).",
)
row(
    "E4a-cmd-pytest",
    "2.5-labs",
    "tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py",
    "PASS",
    f"`.venv/bin/python -m pytest -q` on the three suites -> all tests passed, exit 0 ({LOGS}/pytest_relevant.txt).",
)
row(
    "E4a-cmd-verify_refs",
    "2.1-citations",
    "index.html, L01.html, L02.html, L03.html (data-references)",
    "PASS",
    f"tools/verify_refs.py --offline -> '560 entries, 0 problems' ({LOGS}/verify_refs_offline.txt); tools/verify_refs.py --unit E4 -> 'live re-verification of E4: 3 of 560 entries, 0 problems' ({LOGS}/verify_refs_unit_E4.txt). The slice itself carries 0 data-cite and 0 data-locator attributes (grep), and each lesson's references list is empty by its own text.",
)
row(
    "E4a-hours",
    "2.9-structure",
    "index.html lines 29-43 (data-hours-lessons, data-hours-project); L01 line 2, L02 line 2, L03 line 2",
    "PASS",
    "index.html: data-hours-lessons=\"72\", data-hours-project=\"28\", 72+28=100 (curriculum 100 h, curriculum/02-economics-finance-core.yaml:127). Lessons: data-hours=\"8\" in L01, L02, L03; 9 lessons x 8 = 72 (hub text line 'Nine lessons of eight study hours each').",
)

# ---- numbers (2.2) ----
row(
    "E4a-num-hub",
    "2.2-numbers",
    "index.html lines 68, 71-73, 113-120, 33-38",
    "PASS",
    "Placement item 1: 0*1/4 + 8*3/4 = 6 (expected value in cents, recomputed). Mastery bar 0.8 of 8 items = 6.4, so 7 correct; 6/8 = 75 percent and 7/8 = 87.5 percent (recomputed). Hours split 72/28 = 72 percent and 28 percent of 100 (recomputed). Rung 1 and rung 2 items re-derived: bracket [0, 1/2] for gap positive at 0 and negative at 1/2; G = F_U - e^{ac} F_I (matches project.html Proposition 3, line 287).",
)
row(
    "E4a-num-L01",
    "2.2-numbers",
    "L01.html lines 113-161, 262-281, 320-336, 345-347, 386, 402-404, 448-462, 484-486",
    "PASS",
    f"{SCRIPTS}/rederive_numbers.py (log {LOGS}/rederive_numbers.txt): V(x)=340/3, V(y)=56, E x=235/4, V at pi=235/4, combination 596/3 = 2*340/3 - (1/2)*56, M1: V=55/3, E=25/2, difference 35/6, M3: -1/8, short vector sums to 9/8, Example 1.5 decomposition. Decimals 18.33, 113.33, 58.75, 4.25, 0.6 re-derived; all match.",
)
row(
    "E4a-num-L02",
    "2.2-numbers",
    "L02.html lines 124-126, 187, 192, 299-337, 338, 355-363, 377-393, 429-443, 506-529",
    "PASS",
    f"{SCRIPTS}/rederive_numbers.py: theta = 9/16, 7/16; q* = (1/8, 1/32, 1/16); x1 = (9/4, 9/2, 9/4), x2 = (7/4, 7/2, 7/4); clearing and budget residuals all 0; ratios 16/9 and 16/7; Remark 2.6 at q=(2,1,1): wealths 11 and 9, z=(1,-3,1), unweighted sum -1, q.z = 0; Misconception 2: q*.(1,-1,0) = 3/32; Misconception 3: q*.e1 = 9/16; M2 demand (3/4, 3/8, 3/2), spend 3; prices of states 2 and 3 are 1/32 and 1/16 (Misconception 1).",
)
row(
    "E4a-num-L03",
    "2.2-numbers",
    "L03.html lines 119, 124, 250-261, 301-310, 335-336, 353, 385, 406, 476",
    "PASS",
    f"{SCRIPTS}/rederive_numbers.py: MRS agent 1 and agent 2 (states 12, 13, 23) = 4, 2, 1/2 equal to the price ratios; grid size 125 (5 values, 3 states); improvements at equilibrium 0 (closest gap to threshold 0.0398); improvements at endowment 2, first (2,4,3) and (2,4,1); endowment MRS 8/3 and 8; R2 derivatives 1/12 and 1/4 (recomputed). Log {LOGS}/rederive_numbers.txt.",
)

# ---- mathematics (2.4) ----
row(
    "E4a-math-L01",
    "2.4-mathematics",
    "L01.html lines 77-151, 286-287, 358-361, 393-412",
    "PASS",
    "Re-derived Proposition 1.4 (decomposition), 1.7 (value formula by induction on finite sums with A2), 1.8 (uniqueness via e_s), 1.10 (both directions), Remark 1.11, Example 1.5. Proofs have no gap; A1 used for finiteness. Exercises M1-M3, P1-P3, R1-R3 solutions re-derived step by step.",
)
row(
    "E4a-math-L02",
    "2.4-mathematics",
    "L02.html lines 99-178, 111-116, 128-136, 166-177, 451-455",
    "PASS",
    "Re-derived Lemma 2.4 (y = (w/(2 q.iota)) iota is affordable with finite utility, so demands are positive), Proposition 2.5 (strict monotonicity via pi_s > 0; budgets bind; summation), Corollary 2.7 (now carries the demand hypothesis), Proposition 2.8 (tangent-line inequality, pi_s/x*_s = q_s/w, uniqueness), Proposition 2.9 (theta sums to 1, q*.e-bar = 1, x* = theta e-bar, clearing, wealth theta_i). Each step is a valid inference under the numbered assumptions cited.",
)
row(
    "E4a-math-L03",
    "2.4-mathematics",
    "L03.html lines 81-110",
    "PASS",
    "Re-derived Proposition 3.4 (a) steps 1-3 (Step 1 uses the demand property, Step 2 A4 and A1, Step 3 adds the inequalities and uses feasibility) and (b) (perturbation d = e_s/q_s - e_t/q_t with q.d = 0, derivative G, sign argument). Both proofs are valid for strictly positive equilibrium bundles, which Lemma 2.4 supplies under A1, A3, A4.",
)
row(
    "E4a-math-L03-b-uprime",
    "2.4-mathematics",
    "L03.html line 109 (proof of (b)), line 69 (Definition 3.3)",
    "PASS",
    "Re-derived: u' >= 0 from strict increase; u' nonincreasing from concavity; if u'(x_t)=0 then u'=0 on (x_t, inf), so u is constant there, contradicting strict monotonicity. Hence u'(x_t) > 0 for every x_t > 0 and the ratio in Definition 3.3 is defined.",
)
row(
    "E4a-assumptions",
    "2.4-mathematics",
    "L01.html lines 61, 99; L02.html lines 58, 63, 89, 93; L03.html line 55",
    "PASS",
    "Assumptions A1 to A5 are numbered and stated before use. Each proposition's 'Assume' line lists the ones its proof uses: Prop 1.4 A1; 1.7 A1, A2; 1.8 A1, A2; 1.10 A1, A2; Lemma 2.4 A1, A3, A4; 2.5 A1, A3, A4; 2.8 A1; 2.9 A1, A3 and log utility; 3.4 A1, A3, A4 (with differentiability in (b)).",
)
row(
    "E4a-existence-scope",
    "2.4-mathematics",
    "L02.html lines 51, 84-94, 182, 345; L03.html line 268",
    "PASS",
    "A5 (existence) is a hypothesis and is named wherever needed (Prop 3.4 takes an equilibrium as given). Proposition 2.9 is a construction for the logarithmic economy only. No general existence claim found by reading every sentence.",
)
row(
    "E4a-A2-nonlinear-sources",
    "2.9-prose",
    "L01.html line 104",
    "PASS",
    "Assumption A2 text: quantity discounts, bid-ask spreads and price impact each make V nonlinear. Checked against the definitions: a size-dependent price, a sign-dependent price and a price that depends on trade size are each not additive or homogeneous in the claim, so the statement holds as a qualitative description; no number is asserted.",
)
row(
    "E4a-scope-words",
    "2.9-prose",
    "index.html, L01.html, L02.html, L03.html (every hit of only, always, never, every, any, same, exactly, drives, in general)",
    "PASS",
    "ledgers/E4/scripts/E4-a-r4/grep_checks.sh (log logs/grep_checks.txt) counts 220 whole-word hits of only, always, never, every, any, same, exactly, drives, all across the four pages. The sentences around the 'only', 'always', 'never', 'drives', 'exactly', 'same' and 'in general' hits and the 'every', 'all' and 'any' hits in the proofs, solutions and lab text were read, and each substantive one is backed as stated above. The round-3 failures are fixed: L02 Remark 2.10 now begins 'Under logarithmic utility, demand depends ... only through'; L01 section 9 names the four lab values it reproduces. The remaining 'only' sentences (L01 'the value depends only on q_2' with x_1 = 0; L03 'counts only the grid allocations'; 'each U_i depends only on own bundle' by definition) are backed by a derivation or the definition. The one remaining false scope claim is separate (E4a-r4-P2-only-scope).",
)
row(
    "E4a-r3-walras-demand-existence",
    "2.4-mathematics / rule 6 (hypotheses)",
    "L02.html line 51, line 130 (Corollary 2.7), line 510 (quiz Q3)",
    "PASS",
    "Line 51: 'the value of the excess demand ... is zero at any positive price vector at which each agent has a demand (Proposition 2.5)'. Corollary 2.7 (line 130): 'let x^1 and x^2 be demands at q, so that z(q) is defined'. Quiz Q3 (line 510) now asks about prices 'at which both agents have demands'. The hypothesis is carried in all three places; the \\gg symbol in Q3 is a separate defect (E4a-r4-gg-undefined).",
)
row(
    "E4a-r3-remark26-witness",
    "2.2-numbers / 2.9-prose",
    "L02.html lines 124-126 (Remark 2.6)",
    "PASS",
    "Remark 2.6 now states the witness: at q=(2,1,1) in Example 2.11 the excess demand is (1,-3,1), unweighted sum -1, q.z = 0. Re-derived in rederive_numbers.py (Remark 2.6 block). The claim 'unweighted excess demands need not add to zero' is now supported on the page.",
)
row(
    "E4a-r3-remark210-title",
    "2.2-lab-statements / 2.9-prose",
    "L02.html line 181 (Remark 2.10 title); tests/labs/E4/lab-E4-L02-1.py lines 16-17",
    "PASS",
    "Title is now '(the scale of the price is not fixed by demand)'. The twin's Part E docstring reads 'so demand does not fix the scale of the prices'. The page's expected block matches the twin's output (check_twins_embed.txt).",
)
row(
    "E4a-r3-remark35-hypotheses",
    "2.9-prose / rule 6 (hypotheses list)",
    "L03.html line 114 (Remark 3.5), line 342 (P3 solution), line 448 (quiz Q4 explanation)",
    "PASS",
    "Remark 3.5 now states that (b) uses the strict monotonicity and concavity of A4, which show u_i' is positive. P3 solution and quiz Q4 explanation say the same. Verified against proof of (b), lines 105-109.",
)
row(
    "E4a-L03-M2-scope",
    "2.9-prose",
    "L03.html line 310 (M2 solution)",
    "PASS",
    "Now reads: 'It uses the demand property, the budget, and the differentiability of A4, together with u_i' > 0 from strict monotonicity and concavity.' Matches proof of (b). M2 numbers re-derived: x = (3/2, 3), spend 6, MRS 2 = q1/q2.",
)

# ---- structure and placement (2.9) ----
row(
    "E4a-struct-hub",
    "2.9-structure",
    "index.html lines 66-123 (placement), lines 35, 63 (prerequisites)",
    "PASS",
    "Eight placement items: six prerequisite items (M4 expectation, E2 adverse selection, M7 Lagrange, E1 price-taking, E3 expected utility, M3 linear maps) and two skill items. Each prerequisite module E2, E3, M7 is tested. data-mastery 0.8 and the 7-of-8 arithmetic are on line 68. Objectives: 8 measurable verbs (lines 49-58). Lesson map: 9 cards with titles equal to the lessons' h1 (L01-L03 checked here; L04, L05 h1 equal their card titles).",
)
row(
    "E4a-r3-placement-skill-items",
    "2.9-structure (BUILDER_RULES 5.1)",
    "index.html lines 112-120 (data-skill items 7 and 8); project.html lab-E4-project-2 and lab-E4-project-1 text",
    "PASS",
    "Item 7 (rung 1): bisection bracket for the informed fraction, sign change between 0 and 1/2 (the project's rung 1 prints 'after halving {step}: bracket', lab-E4-project-1 twin line 75). Item 8 (rung 2): the return line F_U - e^{ac} F_I of indifference_gap (project.html line 176 hypothesis; project Proposition 3 line 287, G = F_U - e^{ac}F_I). Both test skills rungs 1 and 2 teach.",
)
row(
    "E4a-hub-placement-explain",
    "2.9-prose",
    "index.html lines 78, 82, 87, 96, 101, 110, 115, 120, 127",
    "PASS",
    "Explanations re-read against the lessons. Item 2 cites E2 Lesson 3 (def-adverse-selection, E2 L03.html) and E2 Lesson 4 (def-signaling, E2 L04.html): both verified by grep. Item 3 cites M7. Item 4 cites Definition 2.2 of L02 (price taking). Item 8 says rung 2 completes the return of indifference_gap, which matches project.html.",
)
row(
    "E4a-r3-hub-CU",
    "2.9-prose / defined terms (plan 2.1 item 8)",
    "index.html lines 71, 73 (placement item 1)",
    "PASS",
    "grep -c -w CU over index.html, L01-L03: 0 hits (logs/grep_checks.txt, CU block). Item 1 is now in cents ('pays 0 cents with probability 1/4 and 8 cents with probability 3/4'; explanation '= 6 cents').",
)
row(
    "E4a-quiz-items",
    "2.9-prose",
    "L01.html lines 437-505; L02.html lines 495-567; L03.html lines 418-486",
    "PASS",
    "All 27 quiz items read (9 per lesson); keys recomputed. L01: 7; 4.25; 2V(x); 3; AD property; A1; 0.6; r=q; size discount. L02: pi_s w/q_s; 2; q.z=0; positive bundle argument; 0.125; theta_i; unchanged; best affordable bundle; one-specification statement. L03: part (a) statement; 2; Pareto definition; differentiability; 2; yes (Example 3.6); efficiency; 4; strict monotonicity. The L02 Q3 prompt now carries the demand hypothesis; its symbol is a separate defect.",
)
row(
    "E4a-r3-L01-references-labs",
    "2.9-prose / rule 4 (scope)",
    "L01.html line 511 (section 9 References)",
    "PASS",
    "Now: 'Lab 1, Parts B to D, reproduces its exact values 340/3, 56, 596/3 and 235/4.' Checked against the twin output: Part B 340/3 and 56, Part C 596/3, Part D 235/4. The other quoted numbers (12.5, 18.33, 35/6, 58.75, 113.33, 4.25, 0.6) are stated as exact hand computations and recomputed in rederive_numbers.py.",
)
row(
    "E4a-banned-phrases",
    "2.9-prose",
    "index.html, L01.html, L02.html, L03.html",
    "PASS",
    "grep -i for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly: 0 hits. Ellipsis appears only inside <code> blocks (Python tuple[Fraction, ...]).",
)
row(
    "E4a-process-words",
    "2.9-prose",
    "index.html, L01.html to L03.html, lab-E4-L01-1 to L03-1",
    "PASS",
    "logs/grep_checks.txt (process-words block): no hit for builder, verifier, REQUEST, unit report, fixer or ledger, and 'round' matches only a rounding statement (the only 'round' is 'no rounding occurs' in the L02 lab hypothesis, which is a rounding statement).",
)
row(
    "E4a-struct-lessons",
    "2.9-structure",
    "L01.html, L02.html, L03.html",
    "PASS",
    f"{SCRIPTS}/structure_counts.py (log {LOGS}/structure_counts.txt): why-it-matters 105, 117, 120 words (<= 120); core sections present; inline lab before canon-breaks; misconceptions 3 per lesson; problem sets M1-M3, P1-P3, E1-E3, R1-R3 in each lesson with 12 solutions of at least 20 words; quiz 9 items each with an explanation; key-results table; references section (no registry key). No debate section required (no debate key).",
)
row(
    "E4a-hub-cards-h1",
    "2.9-structure",
    "index.html lines 129-137; L01-L03 <h1>",
    "PASS",
    "Card titles 'Arrow-Debreu securities and state-contingent payoffs', 'Arrow-Debreu equilibrium', 'The first welfare theorem' equal the h1 of L01, L02, L03 (grep).",
)
row(
    "E4a-hub-cards-h1-L04-L05",
    "2.9-structure",
    "index.html lines 132-133; L04.html and L05.html <h1>",
    "PASS",
    "Card titles 'Complete and Incomplete Markets' and 'Rational-Expectations Equilibrium' equal the h1 of L04 and L05 (grep of <h1> in each file).",
)
row(
    "E4a-hub-prereq-unlock",
    "2.9-structure",
    "index.html lines 35-36, 63",
    "PASS",
    "Prerequisites E2 'Game Theory & Information Economics', E3 'Decision Theory Under Risk & Ambiguity', M7 'Optimization' and unlocks AP1 'No-Arbitrage & the Stochastic Discount Factor', AP6 'Intermediary & Institutional Asset Pricing', MS1 'Microstructure Theory', SR1 'Runs, Liquidity & Fire Sales' equal curriculum/curriculum.json titles; AP1, AP6, MS1, SR1 list E4 as a prerequisite.",
)

# ---- DAG and concepts (2.5, 2.9) ----
row(
    "E4a-hub-introduces",
    "2.5-DAG",
    "L01.html line 74; L02.html line 89; L03.html line 78 (dfn)",
    "PASS",
    "Each introduced concept is defined once with <dfn id=def-<id> data-concept=<id>>: arrow-debreu-security (L01 Definition 1.3), arrow-debreu-equilibrium (L02 Definition 2.3), first-welfare-theorem (L03 Section 2). grep count 1 each in the slice.",
)
row(
    "E4a-dag-outside-closure",
    "2.9-DAG",
    "index.html, L01.html, L02.html, L03.html",
    "PASS",
    "logs/grep_checks.txt (define-before-use block): the only hits are index.html line 36 (Unlocks list, AP1 title) and index.html line 149 (L09 card: 'posteriors as conditional probabilities', plain term, defined in L09 per plan section 12 Q17). No lesson body in the slice uses Bayes, posterior, state price, martingale, CARA, common knowledge, informationally efficient, stochastic discount factor, Banach or intermediate value. Hub lede names 'noise traders' (defined in L06) as overview naming; see notes.",
)
row(
    "E4a-links-earlier-lessons",
    "2.9-DAG",
    "L02.html lines 37, 84, 89; L03.html lines 37, 64, 78",
    "PASS",
    "L02 links only L01 (arrow-debreu-security, L01.html#def-arrow-debreu-security) and prerequisite concepts via ../../../concepts.html#. L03 links L02.html#def-arrow-debreu-equilibrium and L01.html#def-arrow-debreu-security. No link to a later lesson.",
)
row(
    "E4a-define-before-use",
    "2.9-prose / defined terms",
    "L02.html line 51; L03.html line 51; body text of L01-L03",
    "PASS",
    "Each term used in a lesson's body is defined by <dfn> earlier in that lesson or in an earlier lesson (endowment, aggregate endowment, wealth, budget set, demand, Pareto improvement, marginal rate of substitution, interior, Walras' law). Walras' law is defined in Prop 2.5 and referenced in Q3 after it.",
)
row(
    "E4a-define-interior",
    "2.9-prose",
    "L03.html line 51 (first use with dfn), 271, 310, 451",
    "PASS",
    "'interior' is defined by <dfn> at first use in the why-it-matters paragraph of L03 (line 51); later uses are after it.",
)

# ---- labs (2.5) ----
row(
    "E4a-lab-hypothesis-before-output",
    "2.5-labs",
    "L01.html line 160 vs expected line 262; L02.html line 192 vs line 313; L03.html line 124 vs expected line 250",
    "PASS",
    "Each hypothesis states the printed results before the expected block (checked by line order and against the output in check_twins_embed.txt).",
)
row(
    "E4a-lab-L01-statements",
    "2.5-labs",
    "L01.html lines 160, 281; code and twin lines 59-101 (lab-E4-L01-1.py)",
    "PASS",
    "Hypothesis numbers 340/3, 56, 596/3, 235/4, 9/8 and the False flag match the printed output. Interpretation says Part C checks A2 'on that combination only' and that the lab does not show any market prices claims this way: both are true statements about the lab.",
)
row(
    "E4a-lab-L02-statements",
    "2.5-labs",
    "L02.html lines 192, 193-212, 338; tests/labs/E4/lab-E4-L02-1.py",
    "PASS",
    "Hypothesis prices, demands, ratios 16/9 and 16/7, scaling claim, ValueError on zero endowment all match the output. Interpretation: five residuals (two budget, three market clearing) plus Walras are exactly 0; demand falls by 3 with wealth fixed, so the flag depends on re-valuation (algebra checked).",
)
row(
    "E4a-lab-L03-interpretation",
    "2.5-labs",
    "L03.html lines 124, 261; tests/labs/E4/lab-E4-L03-1.py lines 1-20",
    "PASS",
    "Interpretation: 0 improvements of the equilibrium among 125 grid allocations; 2 of the endowment; first witness (2,4,3) and (2,4,1). Confirmed by rederive_numbers.py. 'grade C with that basis' matches the key-results row.",
)
row(
    "E4a-lab-runtime-rng-stdlib",
    "2.5-labs",
    "tests/labs/E4/lab-E4-L01-1.py, L02-1.py, L03-1.py",
    "PASS",
    "Standard library only (fractions, math, itertools, __future__). No random draws (docstrings and code). Each lab runs in 0.0 s in page_smoke. main() called unconditionally at module end, no __main__ guard (grep).",
)
row(
    "E4a-simulated-data",
    "2.8-data",
    "index.html lines 38, 155, 167-168; L01-L03 labs",
    "PASS",
    "No dataset is named or used (curriculum has none for E4; hub 'Data status' says so). The labs use exact illustrative inputs written in code, which are not simulated draws and need no SIMULATED label. Project instances are a slice-e matter.",
)
row(
    "E4a-figures",
    "2.8-figures",
    "index.html, L01.html, L02.html, L03.html",
    "PASS",
    "grep for data-chart, <svg, <figure: 0 hits in all four pages. No figure to verify.",
)
row(
    "E4a-mutants",
    "2.6-grader",
    "tests/labs/E4 (no grader in slice a)",
    "PASS",
    "Not applicable to slice a: index and L01 to L03 have no grader, and lab twins are demonstrations (ruling: mutation testing applies to project graders only). The ten student-error mutants are slice e's duty.",
)
row(
    "E4a-L01-misc2-partA",
    "2.9-prose",
    "L01.html line 307; code line 222 (twin line 62)",
    "PASS",
    "Misconception 3 says Lab 1 checks its unequal probabilities once at the start of main(), before Part A, and that Part A uses only the claim. grep and twin code: check_probabilities(STATE_PROBABILITIES) is called first in main(); Part A reads CLAIM only.",
)
row(
    "E4a-term-additive",
    "2.9-prose",
    "index.html; L01.html lines 7, 51",
    "PASS",
    "grep -i additive over the four pages: 0 hits. No term to check; the row covers the round-3 term-list item, which no longer appears.",
)
row(
    "E4a-L01-R2-title",
    "2.9-prose",
    "L01.html line 401 (title), lines 402-404 (solution)",
    "PASS",
    "Title 'A size effect breaks linearity'. Solution: V(e_1) = 1/4, V(2 e_1) = 1, linearity would need 1/2, so A2 fails. Re-derived.",
)
row(
    "E4a-L01-continuity-necessity",
    "2.9-prose",
    "L01.html line 287 (canon-breaks), line 397 (R1 solution)",
    "PASS",
    "Canon says countable states need an extra condition on V and this lesson does not supply one; R1 solution names the failing step (A2 applied to an infinite sum) and says the formula is not derived here. No sufficient condition is asserted.",
)
row(
    "E4a-L01-P3-title",
    "2.4-mathematics",
    "L01.html line 358 (title), lines 359-361 (solution)",
    "PASS",
    "P3 title 'Prices that differ from probabilities, two states'. Solution: pi=(1/3,2/3), q=(1/4,1/2), V(e_1)=1/4 differs from E e_1 = 1/3; contrapositive of Prop 1.10. Re-derived.",
)
row(
    "E4a-L02-residual-count",
    "2.5-labs",
    "L02.html line 338; expected block lines 313-335",
    "PASS",
    "Interpretation count of five residuals (two budget, three market clearing) and the Walras residual matches the expected block (budget_residual 0 twice, market_clearing_residual 0 three times, walras_law_residual 0).",
)
row(
    "E4a-L02-partE-wealth",
    "2.2-numbers / 2.5-labs",
    "L02.html lines 182, 192, 208, 298-302, 338, 443; twin Part E",
    "PASS",
    "Part E prints demand_unchanged True for both agents with prices scaled by 3 and wealth re-valued (x = pi w / q unchanged). Algebra re-checked: with wealth fixed the demand falls by 3.",
)
row(
    "E4a-L02-partF-docstring",
    "2.5-labs",
    "tests/labs/E4/lab-E4-L02-1.py docstring; L02.html lines 210 and 337",
    "PASS",
    "Part F docstring: zero endowment entry rejected. Printed message 'endowments must be strictly positive in every state' matches the check_economy ValueError text.",
)
row(
    "E4a-L02-uniqueness-z",
    "2.9-prose",
    "L02.html lines 84, 89, 148",
    "PASS",
    "Demand is defined as a maximizer over the budget set (Definition 2.2); z(q) is defined from the chosen demands (Definition 2.3); uniqueness of the logarithmic demand is Proposition 2.8 (exactly one maximizer). Consistent.",
)
row(
    "E4a-L02-CRRA-no-closed-form",
    "2.4-mathematics",
    "L02.html line 346 (canon-breaks)",
    "PASS",
    "The canon says the closed-form formulas do not apply to other A4 utilities (example -1/x) and are not derived there. -1/x does satisfy A4 (strictly increasing, strictly concave, differentiable on (0,inf)), and no closed form is claimed for it.",
)
row(
    "E4a-L02-A4-finite-zero",
    "2.4-mathematics",
    "L02.html line 68",
    "PASS",
    "The convention U_i = -inf at a zero entry; checked that no result uses u_i(0): Lemma 2.4, Prop 2.5, Prop 2.8, Prop 3.4 use either positive bundles or the -inf convention.",
)
row(
    "E4a-wi-positive",
    "2.4-mathematics",
    "L02.html line 120 (proof of Prop 2.5); L03.html line 93 (proof of Prop 3.4 (a))",
    "PASS",
    "w_i = q.e^i > 0 because q is strictly positive (Definition 2.3 domain) and e^i is strictly positive (A3). Re-derived.",
)
row(
    "E4a-L03-remark36",
    "2.9-prose",
    "L03.html line 59 (Definition 3.1); research problem R1 (lines 375-379)",
    "PASS",
    "Definition 3.1 feasibility with equality; R1 changes it to an inequality and names the step using q* >> 0 (last step). Re-derived.",
)
row(
    "E4a-L03-state-labels",
    "2.9-prose / notation",
    "L03.html lines 119, 302, 384, 406, 473; L02 Example 2.11",
    "PASS",
    "States are numbered 1, 2, 3 as in Example 2.11; the lab prints 'states 1 2' for code pair (0,1), as its docstring says.",
)
row(
    "E4a-L03-R3-cannot",
    "2.9-prose",
    "L03.html lines 389-393 (R3 solution)",
    "PASS",
    "At a bundle with a zero entry the one-sided move leaves the orthant and U is -inf under the A4 convention, so the derivative does not exist for that move; equilibrium bundles are strictly positive by Lemma 2.4 (which the solution cites).",
)
row(
    "E4a-L03-lab3-because",
    "2.5-labs",
    "L03.html line 124",
    "PASS",
    "Hypothesis says R2 gives an explicit improvement by hand and the printed count is the evidence for the grid search; R2 exists (line 383) and the count is printed.",
)

# ---- notation (2.4) ----
row(
    "E4a-notation-mathbf1",
    "2.4-notation",
    "L01.html lines 345-347, 486; L02.html lines 106, 120, 525; L03.html lines 105",
    "PASS",
    "The vector of ones is the local symbol iota, defined in each proof where it first appears (L01 P1 defines it, L02 Lemma 2.4 defines it). No \\mathbf{1} is used in the slice.",
)
row(
    "E4a-notation-registered",
    "2.4-notation",
    "index.html, L01.html, L02.html, L03.html",
    "PASS",
    "Registered macros used: \\R (e.g. L02 line 55, L03 line 59) and \\E (L01 Definition 1.9). No \\mathbb{R}, \\mathbb{E}, \\mathbb{Q}, \\Phi, \\gamma, R^\\ast, R_f or T as a symbol (grep). Standard LaTeX commands (\\tfrac, \\cdot, \\sum, \\gg, \\ln) are not registered macros and collide with no registered meaning.",
)
row(
    "E4a-notation-lambda",
    "2.4-notation",
    "index.html lines 117-126 (lambda defined as the informed fraction in Pq7); L02, L03 (no lambda)",
    "PASS",
    "The informed fraction lambda is defined in the placement item where it first appears, and no other meaning is given to it in the slice.",
)
row(
    "E4a-notation-gamma",
    "2.4-notation",
    "L02.html, L03.html, index.html",
    "PASS",
    "grep for gamma: 0 hits in the slice. Nothing to collide with the registered gamma_3, gamma_4.",
)
row(
    "E4a-attribution",
    "2.1-citations / attribution",
    "index.html, L01.html, L02.html, L03.html",
    "PASS",
    "grep for years and named sources (Muth, Milgrom, Stiglitz, Mas-Colell, Econometrica, Journal, 19xx, 20xx): 0 bibliographic hits. Grossman-Stiglitz appears only as the name of a topic (hub objectives and card), not as an attribution. Each lesson's references list is empty and says it cites no registry source.",
)

# ---- the round-4 additions ----
row(
    "E4a-r4-def33-hypothesis",
    "2.4-mathematics / 2.9-prose (hypotheses)",
    "L03.html line 69 (Definition 3.3)",
    "FAIL",
    "Definition 3.3 reads: 'let x be a bundle with x_s > 0 and x_t > 0', then defines MRS as (dU_i/dx_s)/(dU_i/dx_t) = pi_s u'(x_s)/(pi_t u'(x_t)). By A4 U_i(x) = -inf whenever any entry is zero, so for x with x_r = 0 for some r other than s and t the partial derivatives in the definition are not defined. The hypothesis that x is strictly positive in every state is omitted. Proposition 3.4 (b) is only applied at strictly positive bundles (Lemma 2.4), so the theorem is unaffected; the definition is not.",
    "In Definition 3.3 replace 'let x be a bundle with x_s > 0 and x_t > 0' with 'let x be a strictly positive bundle (x_r > 0 for every state r)'. Keep the rest of the definition unchanged.",
)
row(
    "E4a-r4-gg-undefined",
    "2.9-prose / notation (define before use)",
    "L02.html line 466 (Problem R3 prompt), line 510 (quiz Q3); L03.html line 93 (proof of Prop 3.4 (a)), line 376 (R1 prompt), line 378 (R1 solution)",
    "FAIL",
    "The symbol \\gg (x >> 0) appears on five lines of L02 and L03 and is never defined on either page (grep -F '\\gg' in logs/grep_checks.txt gives exactly these lines: L02 466 and 510; L03 93, 376 and 378). Its meaning is 'every entry strictly positive', which the pages use in words elsewhere (Lemma 2.4 states 'x_s > 0 for every state'). It is not a registered notation macro and no registry meaning conflicts with it, so this is a define-before-use defect, not a notation collision.",
    "At the first use (L02 line 466) add the sentence 'We write x >> 0 when x_s > 0 for every state s.' Alternatively replace each \\gg 0 by the words 'strictly positive', which is how Lemma 2.4 and Proposition 2.5 state it.",
)
row(
    "E4a-r4-P2-only-scope",
    "2.9-prose (rule 4, scope words)",
    "L03.html lines 333-335 (problem P2 prompt and solution)",
    "FAIL",
    "The prompt says 'show that MRS = q*_s/q*_t ... using only the formulas of Proposition 2.9'. The solution uses u_i'(x) = 1/x, which is the derivative of the logarithm and is not a formula of Proposition 2.9. The 'only' is therefore false for the proof given. The computation itself is correct: MRS = (pi_s e-bar_t)/(pi_t e-bar_s) = q*_s/q*_t with theta_i cancelling (re-derived).",
    "Change the prompt to 'using the formulas of Proposition 2.9 and the derivative of the logarithm, u_i'(x) = 1/x'. Keep the solution.",
)
row(
    "E4a-r4-uses-meta",
    "2.5-DAG (Uses meta-rows)",
    "L02.html line 37 (Uses: lagrange-multiplier, derivative); L03.html line 37 (Uses: gradient)",
    "PASS",
    "Each declared concept is in E4's prerequisite closure (no DAG defect). Note, not a rule violation: L02's prose does not use the Lagrange multiplier or the derivative as a named tool (demand is characterised by the tangent-line inequality), and L03's prose does not use the gradient (it uses the derivative u_i' without declaring it). The builder may tidy the Uses lists; no row fails on this.",
)


out = {
    "unit": "E4",
    "slice": "a",
    "round": 4,
    "verifier": "Haiku independent verifier, E4-a round 4 (did not build E4; no shared context with the builders)",
    "pin": "9a02b1af9f92a060f7fabf7e1b3afb5ea95f45ba",
    "base": "67a2d13e7575608e95b2e34a9c7c2a82c61b117b (round-3 pin). Delta since the base in the slice: index.html 46 lines, L02.html 26 lines, L03.html 12 lines, L01.html 2 lines, lab-E4-L02-1.py 2 lines; lab-E4-L01-1.py and lab-E4-L03-1.py byte-identical to the base (git diff empty). Every round-3 row id is kept; each was re-verified from the text this round (the whole slice was read line by line), not carried.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE4-E4-a (detached at 9a02b1a; .venv symlinked)",
    "scratch": "/tmp only for twin runs (cwd /tmp, python -I -W error). Scripts and logs under ledgers/E4/scripts/E4-a-r4/ (check_twins_embed.py, rederive_numbers.py, structure_counts.py, write_fragment_r4.py, logs/).",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice read in full: index.html (173 lines), L01.html (524), L02.html (586), L03.html (505), twins lab-E4-L01-1.py, lab-E4-L02-1.py, lab-E4-L03-1.py. Every sentence of prose, every proof, every solution, every quiz explanation and every lab hypothesis/interpretation was read; every number was recomputed (rederive_numbers.py).",
        "All 13 round-3 FAIL rows are fixed in the text and re-verified PASS (E4a-math-L02, E4a-scope-words, E4a-r3-walras-demand-existence, E4a-r3-remark26-witness, E4a-r3-remark210-title, E4a-r3-remark35-hypotheses, E4a-L03-M2-scope, E4a-struct-hub, E4a-r3-placement-skill-items, E4a-hub-placement-explain, E4a-r3-hub-CU, E4a-quiz-items, E4a-r3-L01-references-labs).",
        "Plan deviation (non-blocking, for the architect): plan section 1 specifies lab-E4-L02-1 as a two-state economy; the built lab and Example 2.11 use three states. The three-state economy is internally consistent and every number checks, so no row fails on it.",
        "Hub overview names 'noise traders' (lede) and the Arrow-Debreu securities before their lesson definitions. Judged as overview naming, since the hub's first-appearance <dfn> rule (BUILDER_RULES 8) is applied to lesson bodies; the architect may want a link on first hub use.",
        "Housekeeping: round-4 log files named check_pages.py_--unit_E4.txt and similar are the superseded output of a mistyped first invocation; they are overwritten with a one-line note. Removal was blocked by the safety check, so they remain as notes.",
        "Could not check: the live Crossref run of verify_refs over the whole registry (only the unit run, which had 3 entries in scope, and the offline integrity run were executed); the cards (slice f), the project and grader (slice e), and lessons L04-L09 (other slices) were not read, except for the hub's card titles and the L04/L05 h1 strings.",
    ],
    "summary": {},
}

passes = sum(1 for r in rows if r["status"] == "PASS")
fails = sum(1 for r in rows if r["status"] == "FAIL")
unver = sum(1 for r in rows if r["status"] == "UNVERIFIABLE")
out["summary"] = {"rows": len(rows), "pass": passes, "fail": fails, "unverifiable": unver, "mutants_killed": 0, "mutants": 0}

path = ROOT / "ledgers" / "E4" / "E4-a.json"
path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(path, out["summary"], out["verdict"])
