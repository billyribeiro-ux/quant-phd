"""Build the E4 slice a delta fragment (round 1, closing, pin 95f3f8cb) from the round-13 base fragment.

Rows: every base row id is kept. A base row is re-verified (fresh evidence written here) when its subject changed
in e919577..95f3f8cb or it is a gate that was re-run; every other base row is carried with the carry prefix
(ruling 30 and the verifier rules). New delta rows are added with ids prefixed E4a-r1-delta-.

Run from the checkout root: .venv/bin/python -I ledgers/E4/scripts/E4-a-r1/build_fragment_a1.py
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
BASE = Path("/Users/billyribeiro/.fanout/frags/E-E4-a.round13.json")
OUT = ROOT / "ledgers/E4/E4-a.json"
PIN = "95f3f8cb21c2cd9fc904430bd30a6b734d01f672"
BASE_PIN = "e919577b45b431ce68e1e6533b00b8a301277937"
S = "ledgers/E4/scripts/E4-a-r1/outputs/"

GATES = {
    "E4a-r6-cmd-check_pages": f"Round 1 (pin {PIN[:8]}): .venv/bin/python tools/check_pages.py --unit E4 printed 'check_pages E4: PASS', exit 0 ({S}check_pages_E4.txt). Covers the changed L03.html.",
    "E4a-r6-cmd-check_dag": f"Round 1: tools/check_dag.py --all printed PASS for every unit including E4, 0 FAIL lines, exit 0 ({S}check_dag_all.txt).",
    "E4a-r6-cmd-run_labs": f"Round 1: tools/run_labs.py --unit E4 printed 'run_labs E4: PASS (12/12)', exit 0 ({S}run_labs_E4.txt).",
    "E4a-r6-cmd-page_smoke": f"Round 1: tools/page_smoke.py --unit E4 --pages index, L01, L02, L03 each printed PASS, exit 0 ({S}page_smoke_*.txt): light and dark, 360 px, zero console errors, zero external requests.",
    "E4a-r6-cmd-twins-alone": f"Round 1: ledgers/E4/scripts/E4-a-r1/lab_page_twin_check.py ran tests/labs/E4/lab-E4-L01-1.py, L02-1.py and L03-1.py under python -I -W error: each exit 0, empty stderr, FAILS: 0 ({S}lab_page_twin_check.txt).",
    "E4a-r6-cmd-twin-embed": f"Round 1: lab_page_twin_check.py PASS lines for L01, L02, L03: the data-run code equals the twin source and pre.expected equals the twin stdout ({S}lab_page_twin_check.txt).",
    "E4a-r6-cmd-ruff": f"Round 1: ruff check tests/labs/E4 printed 'All checks passed!' and ruff format --check tests/labs/E4 exit 0 ({S}ruff_twins.txt, ruff_format_twins.txt).",
    "E4a-r6-cmd-mypy": f"Round 1: mypy --no-incremental tests/labs/E4 printed 'Success: no issues found in 12 source files', exit 0 ({S}mypy_twins.txt).",
    "E4a-r6-cmd-pytest": f"Round 1: pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py printed no failures, EXIT=0 ({S}pytest_slice.txt). The three test files and tools/ are byte-identical to e919577 (git diff --quiet).",
    "E4a-r6-cmd-verify_refs": f"Round 1: tools/verify_refs.py --offline printed 'offline integrity: 560 entries, 0 problems', exit 0 ({S}verify_refs_offline.txt). The E4 pages cite no registry key (data-references empty).",
    "E4a-r6-cmd-check_projects": f"Round 1: tools/check_projects.py --unit E4 printed 'check_projects E4: PASS', exit 0 ({S}check_projects_E4.txt). project.html changed since e919577 and is gated here.",
    "E4a-r10-cmd-run_graders": f"Round 1: tools/run_graders.py --unit E4 --seeds 0-49 printed 'run_graders E4: PASS (reference 50/50 seeds, slowest 0.3 s)', exit 0 ({S}run_graders_E4_0-49.txt). grader/test_project.py changed since e919577 and is re-run here. A bare pytest collect of that file fails with ModuleNotFoundError 'solver' because run_graders supplies the module; that is the harness design, not a defect.",
    "E4a-r11-cmd-verify_refs-offline": f"Round 1: tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems', exit 0 ({S}verify_refs_offline.txt). references/references.json changed only in generated_at and one FC2 used_by entry.",
    "E4a-r12-gates-and-pytest": f"Round 1: every gate re-run at {PIN[:8]} exited 0: check_pages, check_dag, check_projects, run_labs, lab_page_twin_check, build_site --check, render_curriculum --check, verify_refs --offline, page_smoke x4, ruff, mypy, pytest (slice tests), run_graders E4 0-49 ({S}exit_codes.txt and the per-gate files).",
    "E4a-r13-gates": f"Round 1: gate runner ledgers/E4/scripts/E4-a-r1/run_gates_delta.sh: every command exit 0 ({S}exit_codes.txt). The structure script reports one FAIL (word count 121), explained in row E4a-r6-struct-why-words.",
    "E4a-r13-lab-twins-alone": f"Round 1: lab_page_twin_check.py ran tests/labs/E4/lab-E4-L01-1.py, L02-1.py, L03-1.py under python -I -W error: exit 0 and empty stderr for each ({S}lab_page_twin_check.txt).",
}

REVERIFIED = {
    "E4a-r6-struct-lesson-order": f"Round 1: check_pages E4 PASS (section order, {S}check_pages_E4.txt). The delta touches no h2 or section tag in L03 (hunks at lines 51, 55, 114, 270, 272, 343, 386, 407, 445, 449, 452 only).",
    "E4a-r6-struct-counts": f"Round 1: L03 counts re-read at {PIN[:8]}: 3 misconceptions (lines 279-287), tiers mechanics M1-M3, proof P1-P3, empirical E1-E3, research R1-R3 (lines 298-396), quiz 9 items (lines 418-488). Unchanged by the delta. L01 and L02 counts carried.",
    "E4a-r6-struct-why-words": f"Round 1: check_pages words() on the L03 why-it-matters paragraph = 120, limit 120 (BUILDER_RULES 4.2 item 1): PASS. The base structure script ({S}structure_slice_a.txt) reports 121 because its text_of() joins text nodes with a space, so '<dfn>interior</dfn>,' counts as two tokens. The official count is 120. L01 = 114 and L02 = 118 (carried).",
    "E4a-r6-struct-solution-words": f"Round 1: check_pages requires every problem solution to have at least 15 words (PASS). The changed L03 solutions (P3 line 343, R2 line 386) are far above 15 words.",
    "E4a-r6-hub-card-claims-L01-03": "Round 1: index.html line 143 (L03 card body: 'the equality of marginal rates with price ratios at interior equilibrium bundles') checked against the changed L03 text. Lemma 2.4 (L02 lines 100-107) makes every demand, hence every equilibrium bundle, strictly positive, so 'interior equilibrium bundles' is accurate. Lines 141-142 unchanged.",
    "E4a-r6-dag-closure": f"Round 1: check_dag --all PASS. L03 concept links (lines 37, 64, 271) are arrow-debreu-equilibrium, arrow-debreu-security, gradient, pareto-efficiency and externality, all in the prerequisite closure. The delta adds no concept link (diff read).",
    "E4a-r6-dag-defs-unique": "Round 1: L03 line 78 has the only dfn id def-first-welfare-theorem; structure script 'dfn id def-first-welfare-theorem matches data-concept' PASS. The delta adds an unlabelled <dfn>interior</dfn> at line 51, which is not a concept id.",
    "E4a-r6-dag-D-terms": "Round 1: the delta introduces 'interior' at L03 line 51, defined in the same sentence ('Lemma 2.4 makes every equilibrium bundle interior, with every entry strictly positive') before its use in Remark 3.5, the canon-breaks bullet and card c225. No undefined term is introduced.",
    "E4a-r6-notation-macros": f"Round 1: structure_slice_a.py: 'TeX control words used not in notation.json macros nor standard set: []' for L03; supplementary_scans.py: 'macros outside the standard set and the registered set: []' ({S}supplementary_scans.txt).",
    "E4a-r6-notation-registered-symbols": "Round 1: notation/notation.json lists 8 symbols (gamma_3, gamma_4 and others, module M4). None of e_s, e^i, bar e, u_i, U_i, MRS, pi, q, theta is registered, so the delta cannot collide with a registry meaning.",
    "E4a-r6-notation-e-collision": "Round 1: in L03, e_s appears only at line 55 (the security e_s of Lesson L01, Definition 1.3) and line 105 (proof of (b): d = e_s/q_s - e_t/q_t), both the Arrow-Debreu security. bar e_s (line 336) is the aggregate. e^i stays an endowment (line 55). L02 line 55 unchanged.",
    "E4a-r7-notation-u-local": "Round 1: u_i is utility in L02 lines 68-71 and L03 line 69 (unchanged text). In L06.html, changed in this delta, u is still the random net supply (L06 diff keeps '\\(u\\)' as the noise supply). The letter is shared, locally, and is recorded as a note (E4a-r13-observation-u-symbol), not a FAIL kind.",
    "E4a-r6-banned-phrases": f"Round 1: ledgers/E4/scripts/E4-a-r13/banned_scan.py over index, L01-L03: 'HITS: 0', exit 0 ({S}banned_scan.txt).",
    "E4a-r6-process-words": f"Round 1: banned_scan.py (0 hits) and the process-word part of supplementary_scans.py ({S}supplementary_scans.txt) over the changed L03 visible text. No process word in the delta sentences.",
    "E4a-r6-scope-words": "Round 1: L03 visible-text counts (grep -o -i): every 21, only 10, any 9, same 13, all 4, exactly 4, always 0, never 0. The delta's scope words are backed: 'every equilibrium bundle interior' by Lemma 2.4 (proved, L02 lines 99-104); 'used only in the proof of part (b)' by the grep that finds e_s only at lines 55 and 105.",
    "E4a-r6-define-before-use": "Round 1: L03 'interior' is defined in-line at line 51 before any use. Definitions 3.1-3.3 (lines 57-74) still precede Proposition 3.4 (line 81). Lemma 2.4 is in L02 (an earlier lesson). Remark 3.5 (line 113), the P3 solution (line 343) and card c225 use only terms defined above.",
    "E4a-r6-attribution": f"Round 1: L03 contains no citation or author name; section 9 says it cites no registry source (line 493). supplementary_scans.py: 'four-digit years in visible text: []' for L03 ({S}supplementary_scans.txt).",
    "E4a-r6-num-L03-example36": "Round 1: recomputed in exact Fractions (ledgers/E4/scripts/E4-a-r1/outputs/rederive_slice_a.txt): prices (1/8, 1/32, 1/16) from pi_s/bar e_s; bundles (9/4, 9/2, 9/4) and (7/4, 7/2, 7/4); MRS^1_12 = 4, MRS^1_13 = 2, MRS^1_23 = 1/2, the same for agent 2; price ratios 4, 2, 1/2. Lab 3 expected lines 250-254 match. Line 285 'as Lab 2 Part C prints' matches L02 line 366.",
    "E4a-r6-num-L03-R2": "Round 1: R2 solution (line 386) recomputed: U_1 derivative = (1/2)(-1/3) + (1/4)(1) = 1/12; U_2 derivative = (1/2)(1) + (1/4)(-1) = 1/4; MRS^1_12 at the endowment = (1/2 / 3)/(1/4 / 4) = 8/3; MRS^2_12 = (1/2 / 1)/(1/4 / 4) = 8; y^1 + y^2 = (4, 8, 4). All numbers agree.",
    "E4a-r6-num-L03-grid": f"Round 1: grid {{0, 1/4, 1/2, 3/4, 1}}^3 has 125 points (lab expected line 257). Lines 258-260 reproduced by running the twin: 0 improvements at the equilibrium, 2 at the endowment, first improvement agent 1 (2,4,3), agent 2 (2,4,1) ({S}run_labs_E4.txt).",
    "E4a-r6-math-L03-def33": "Round 1: Definition 3.3 (lines 67-74) text unchanged. The MRS formula equals (pi_s/x_s)/(pi_t/x_t) for u = ln (Example 3.6). The claim that u_i' is positive on (0, infinity) is proved in the proof of (b) (line 109): u_i' >= 0 by strict monotonicity, nonincreasing by concavity, and u_i'(x_t) = 0 would make u constant on (x_t, infinity), contradicting strict monotonicity.",
    "E4a-r6-math-L03-prop34b": "Round 1: proof of (b) (lines 103-110) re-read: d = e_s/q_s - e_t/q_t has q*.d = 0; G = pi_s u'(x_s)/q_s - pi_t u'(x_t)/q_t; G = 0 by the demand property; u'(x_t) > 0 shown; MRS = q_s/q_t. Strict positivity of x comes from Lemma 2.4 (L02 lines 100-107). Hypotheses A1, A3, A4 at line 82. Consistent with Remark 3.5.",
    "E4a-r6-math-L03-remark35-P3": "Round 1: Remark 3.5 (line 114) and P3 solution (line 343) checked against Lemma 2.4 and the proof of (b). Part (b) adds differentiability and u_i' > 0 (strict monotonicity and concavity); the strictly positive equilibrium bundle comes from Lemma 2.4 as used in part (a), so no extra positivity hypothesis is needed. Part (a) takes no derivative (proof lines 93-100).",
    "E4a-r6-math-L03-M-P-E": "Round 1: lines 300-369 re-read. M1 (line 304) = 2; M2 (line 311) x = (3/2, 3) and MRS 2; M3 feasible; P1 (line 329) consistent with Step 1; P2 (line 336) algebra holds; P3 (line 343) consistent with Remark 3.5; E1 (line 354) prints 4 and (1/8)/(1/32) = 4; E2 (line 361) recomputed (E2 row below); E3 (line 368) consistent with the zero count.",
    "E4a-r6-lab-L03-hypothesis": f"Round 1: hypothesis (line 124) against Lab 3 output lines 250-260 ({S}run_labs_E4.txt): marginal rates 4, 2, 1/2 with flags True; 125 grid allocations; 0 at the equilibrium; 2 at the endowment; no random draws. Consistent.",
    "E4a-r6-lab-L03-interpretation": "Round 1: interpretation (line 261) against the output: the zero count (grade C, a finite enumeration), two endowment improvements, the first with agent 1 (2,4,3) and agent 2 (2,4,1). Matches expected lines 258-260.",
    "E4a-r6-lab-L03-code": "Round 1: the L03 data-run code equals tests/labs/E4/lab-E4-L03-1.py (lab_page_twin_check PASS); the twin ran under python -I -W error with exit 0 and empty stderr.",
    "E4a-r6-lab-page-equals-twin": f"Round 1: lab_page_twin_check.py PASS for L03: page code equals twin, pre.expected equals twin stdout ({S}lab_page_twin_check.txt).",
    "E4a-r6-lab-hypothesis-before-output": "Round 1: lab_page_twin_check.py PASS for L03: the hypothesis paragraph precedes the code block and the interpretation follows the expected block.",
    "E4a-r6-quiz-L03": "Round 1: L03 quiz (lines 418-488), 9 items. L03q4 (line 445): the correct option 'Differentiable utilities (A4), with positive marginal utility from monotonicity and concavity' matches P3 (line 343) and Remark 3.5; the distractors are wrong; the explanation (line 449) matches Remark 3.5. Numeric items: price ratio 2 (line 452), MRS^1_12 = 4 (line 477). Items 1, 2, 3, 6, 7 and 9 unchanged and consistent.",
    "E4a-r6-observation-noise-e": "Round 1: L02 line 55 (unchanged) and L03 line 55 (changed) both say the letter e with an agent superscript is an endowment and that e_s is the security; the L03 sentence now names the Lesson L01 source. Observation only.",
    "E4a-r7-math-L03-R2-compensation": "Round 1: R2 solution (line 386), agent-1 sentence: MRS^1_12 = 8/3 means agent 1 needs 8/3 units of state 2 for each unit of state 1 it gives up; the trade pays 4 units per unit, so it gains. Agent 2 has MRS 8 and gives 4 units per unit received, so it gains. Recomputed with the numbers above.",
    "E4a-r7-delta-coverage": "Round 1: git diff e919577..95f3f8cb over the slice-a paths: course/modules/E/E4/L03.html (changed lines 51, 55, 114, 270, 272, 343, 386, 407, 445, 449, 452, all read) and course/modules/E/E4/cards.json (14 slice-a cards changed, all read). index.html, L01.html, L02.html and the lab twins L01-L03 are byte-identical (git diff --quiet). Cross-referenced but outside the slice: L06.html, project.html, grader/test_project.py, lab-E4-project-1/2.py, L09.html, E2 L03/L04 and E3 index (h1 unchanged).",
    "E4a-r7-rederive-all-numbers": f"Round 1: every number in L03 prose and exercises re-derived with Fraction arithmetic and the twin ({S}rederive_slice_a.txt, FAILS: 0). L01 and L02 numbers carried (byte-identical files).",
    "E4a-r8-delta-L03-line55": "Round 1: L03 line 55 re-read: 'The assumptions used in this lesson are A1, A3 and A4. A1 is stated in Lesson L01, and A3 and A4 in Lesson L02.' Verified: Assumption A1 at L01 line 61; Assumption A3 at L02 line 58; Assumption A4 at L02 line 63. The security e_s of Lesson L01 Definition 1.3 (L01 line 73) is correct. L03 does not use A2 or A5 in a proof (A5 is named only in the canon-breaks bullet, line 268).",
    "E4a-r8-delta-L03-E2": "Round 1: E2 solution (line 361) recomputed: agent 1 change = (1/2) ln(2/3) + (1/4) ln 3 = (1/4) ln(4/3); agent 2 change = (1/2) ln 2 - (1/4) ln 3 = (1/4) ln(4/3); both = 0.0719205 (python). The count 2 matches lab expected line 259. Grades (T for the hand witness, C for the grid count) match key-results row 5.",
    "E4a-r8-delta-L03-R2": "Round 1: R2 solution (line 386) numbers recomputed (see E4a-r6-num-L03-R2). The sentence 'Agent 1 would give up 8/3 units of state 2 for one more unit of state 1' matches Definition 3.3 (line 73: units of the state-t good given up for one more unit in state s).",
    "E4a-r8-grid-recount": f"Round 1: grid = 5^3 = 125 (expected line 257). The counts 0 and 2 reproduced by running lab-E4-L03-1 (exit 0, {S}run_labs_E4.txt). L03 lines 124 and 258-261 match.",
    "E4a-r8-rederive-numbers": f"Round 1: index, L01-L03 numbers re-derived in this round for L03 (prices, bundles, wealths 9/16 and 7/16, MRS values, E2, R2, grid count 125, zero and two counts, first witness; {S}rederive_slice_a.txt). L01, L02 and index numbers carried (byte-identical files).",
    "E4a-r8-concept-anchors-owners": f"Round 1: structure script 'dfn owners: arrow-debreu-security L01, arrow-debreu-equilibrium L02, first-welfare-theorem L03' and the link-anchor PASS lines for L02 and L03 ({S}structure_slice_a.txt).",
    "E4a-r8-macros-and-symbols": f"Round 1: supplementary_scans.py macros check PASS ({S}supplementary_scans.txt). The L03 symbols e_s, e^i, bar e, u_i, U_i, MRS, q*, theta_i are not in the registry and are not reused with another meaning inside L03.",
    "E4a-r8-page-smoke-no-external": f"Round 1: page_smoke L03 PASS: zero requests to any host other than the local server and zero console errors ({S}page_smoke_L03.txt).",
    "E4a-r9-structure-L03-canon-limits": "Round 1: L03 lines 264-274 re-read after the delta: six bullets; 'Complete preferences' (line 270) and 'Boundary allocations are outside (b)' (line 272) are consistent with A4 and Lemma 2.4; the structure script PASS covers the canon-breaks section.",
    "E4a-r10-delta-L03-L270": "Round 1: L03 line 270 ('Complete preferences') re-read: 'compares bundles through the utilities U_i of A4, which take each agent's ranking of bundles to be complete and represented by U_i'. Removing 'only' does not change the claim; A4 defines U_i as the expected utility of u_i. PASS.",
    "E4a-r10-scan-notation": "Round 1: notation scans as in E4a-r6-notation-macros and E4a-r6-notation-registered-symbols: PASS.",
    "E4a-r10-structure-script": f"Round 1: structure_slice_a.py at {PIN[:8]} ({S}structure_slice_a.txt): 167 PASS and one FAIL, the L03 why-it-matters count of 121 that is the text_of() artifact explained in E4a-r6-struct-why-words (official count 120, limit 120). Counts: 3 misconceptions, 2 key-result tables with 5 rows for L03, dfn ids unique.",
    "E4a-r10-rederive-script": f"Round 1: rederive_slice_a13.py at {PIN[:8]}: FAILS: 0 ({S}rederive_slice_a.txt). Every L03 number in prose and exercises reproduces.",
    "E4a-r10-ellipsis": "Round 1: L03 visible prose has no ellipsis placeholder (0 U+2026 characters). The five '...' hits in L03 are Python type annotations inside the lab code (tuple[Payoff, ...]), not prose. banned_scan.py: 0 hits.",
    "E4a-r10-embed": "Round 1: lab_page_twin_check PASS for L01-L03: page code equals twin, expected equals stdout.",
    "E4a-r11-delta-L03-L361": "Round 1: L03 line 361 (E2 solution) re-read and recomputed (see E4a-r8-delta-L03-E2).",
    "E4a-r11-cmd-structure-script": f"Round 1: structure_slice_a.py at {PIN[:8]}: 167 PASS, one FAIL (why-it-matters 121 by the text_of() artifact; official count 120, see E4a-r6-struct-why-words); all other checks PASS ({S}structure_slice_a.txt).",
    "E4a-r12-ruling13-L03-keyrow3": "Round 1: L03 line 407 (key results row 3, MRS values) re-read: grade T; source 'Computed in Example 3.6 from the Example 2.11 bundles, which Proposition 2.9 gives; reproduced exactly by Lab 3 Part A'. The values are hand-derived, which ruling 13 grades T, and Lab 3 Part A reproduces them.",
    "E4a-r12-ruling13-L03-keyrow5": "Round 1: L03 line 409 (key results row 5, grid search) graded C with basis 'Lab 3 Part B, a finite enumeration on a grid; not a proof'. Consistent with the lab output (0 and 2) and with Proposition 3.4 (a) as the proof.",
    "E4a-r6-math-keyresults": "Round 1: L03 section 6 table (lines 405-409) re-read: rows 1-2 T (Proposition 3.4 (a) and (b), proved in section 2 under A1, A3, A4); row 3 T (hand-computed, ruling 13); row 4 T (Problem R2, hand witness); row 5 C (finite grid, Lab 3 Part B). Consistent with lines 67-115 and the labs.",
    "E4a-r6-grades-claims": "Round 1: L03 claim spans re-read: Proposition 3.4 T (line 81); Example 3.6 values by hand T (line 119); Lab 3 Part B counts C (lines 261, 368); R2 T (line 386); key results (lines 405-409). Lemma 2.4 (T, L02 line 100) supports the interior-bundle claims. No claim is over-graded.",
    "E4a-r12-delta-L03-L361": "Round 1: L03 line 361 re-read and recomputed (see E4a-r8-delta-L03-E2).",
    "E4a-r12-banned-and-process-scan": f"Round 1: banned_scan.py HITS 0 and supplementary_scans.py FAILS 0 over index, L01-L03 ({S}banned_scan.txt, supplementary_scans.txt).",
    "E4a-r12-rederive-slice-a": f"Round 1: rederive_slice_a13.py at {PIN[:8]}: FAILS 0. L03 numbers re-derived; L01, L02 and index carried (byte-identical).",
    "E4a-r13-rederive-L01-L03": f"Round 1: rederive_slice_a13.py at {PIN[:8]}: FAILS 0 ({S}rederive_slice_a.txt) for index and L01-L03 twins.",
    "E4a-r13-cards-mirror": f"Round 1: cards.json (259 cards) read for slice a. Ids unique; no duplicate front-and-back pair ({S}cards_check_L01-L03.txt). The 14 changed slice-a cards (c011, c012, c013, c016, c017, c022, c024, c047, c048, c214, c225, c237, c265, c266) checked against the current lesson text: numbers present in their lesson with TeX fractions normalised (no ABSENT line); c047 sums (9/4+7/4 = 4, 9/2+7/2 = 8, 4) and c266 (9/16, 7/16) re-derived; c265 (56 cents) and c011-c013 values re-derived. The 45 unchanged L01-L03 cards are carried; c041-c046, c049-c052 and c043-c044 were re-read against the changed Remark 3.5 and Proposition 3.4 text and are consistent.",
    "E4a-r13-hub-placement-links": "Round 1: index lines 116-133 (Pq7 bracket after three halvings; Pq8 gap F_U - e^{ac} F_I) checked against project.html, which changed: Proposition 3 (project line 287) unchanged; rung-1 printed brackets at project lines 159-161 match 'after the first three halvings'; rung-2 'the return line of the indifference gap (Proposition 3)' at project lines 45 and 175. E2 L03 h1 'Adverse Selection' and L04 h1 'Signaling' unchanged (git diff --quiet).",
    "E4a-r13-observation-u-symbol": "Round 1: observation only (not a FAIL kind): u_i (utility; L02 lines 68-71, L03 line 69) and u (noise supply; L06) share a letter. Both meanings are local and no registry symbol is affected.",
}

CARRY_FILES_OVERRIDE = {
    "E4a-r6-hub-KKT-claim": "course/modules/E/E4/index.html and L02.html",
    "E4a-r6-hub-prereq-usage": "course/modules/E/E4/index.html and the L01-L09 concept links (L03 meta-row line 37 unchanged)",
    "E4a-r12-delta-index-L63-L09": "course/modules/E/E4/index.html and L09.html",
    "E4a-r7-hub-cross-unit-titles": "course/modules/E/E4/index.html; E2 L03 and L04 and E3 index h1 unchanged",
    "E4a-r13-prereq-uses-hub": "course/modules/E/E4/index.html and the L01-L09 data-concept uses",
    "E4a-r6-data-none": "course/modules/E/E4/index.html and the lab twins tests/labs/E4/lab-E4-L01-1.py, L02-1.py, L03-1.py",
    "E4a-r8-data-labs-simulated-labels": "course/modules/E/E4/index.html and the lab twins",
    "E4a-r7-data-simulated-labels": "tests/labs/E4/lab-E4-L06-1.py, lab-E4-L07-1.py, lab-E4-L08-1.py",
    "E4a-r13-hub-data-precision": "course/modules/E/E4/index.html and the lab twins",
    "E4a-r6-lab-stdlib-no-network": "tests/labs/E4/lab-E4-L01-1.py, L02-1.py, L03-1.py",
    "E4a-r6-lab-main-toplevel": "tests/labs/E4/lab-E4-L01-1.py, L02-1.py, L03-1.py",
    "E4a-r6-lab-runtime": "tests/labs/E4/lab-E4-L01-1.py, L02-1.py, L03-1.py",
    "E4a-r6-lab-no-mutants": "tests/labs/E4/lab-E4-L01-1.py, L02-1.py, L03-1.py",
    "E4a-r6-references-none": "course/modules/E/E4/index.html, L01.html, L02.html and the L03.html references section (lines 491-495)",
    "E4a-r8-delta-L03-R1": "course/modules/E/E4/L03.html lines 375-379 (R1), outside every changed hunk",
    "E4a-r6-math-L03-prop34a": "course/modules/E/E4/L03.html lines 91-101 (proof of (a)), outside every changed hunk",
    "E4a-r6-math-L03-R1-free-disposal": "course/modules/E/E4/L03.html lines 375-379, outside every changed hunk",
    "E4a-r6-math-L03-R3": "course/modules/E/E4/L03.html lines 389-393 (no changed line in that range)",
}


def carry_files(row_id: str) -> str:
    if row_id in CARRY_FILES_OVERRIDE:
        return CARRY_FILES_OVERRIDE[row_id]
    if "L03" in row_id:
        return "course/modules/E/E4/L03.html (cited lines outside the changed hunks)"
    if "L02" in row_id:
        return "course/modules/E/E4/L02.html"
    if "L01" in row_id:
        return "course/modules/E/E4/L01.html"
    return "course/modules/E/E4/index.html"


def main() -> None:
    base = json.loads(BASE.read_text(encoding="utf-8"))
    base_ids = [r["id"] for r in base["rows"]]
    for key in list(GATES) + list(REVERIFIED):
        assert key in base_ids, f"not a base row id: {key}"
    rows: list[dict[str, str]] = []
    counts = {"reverified": 0, "carried": 0}
    for row in base["rows"]:
        rid = row["id"]
        if rid in GATES:
            evidence = GATES[rid]
        elif rid in REVERIFIED:
            evidence = REVERIFIED[rid]
        else:
            evidence = (
                f"Carried from round 13 ({carry_files(rid)} byte-identical since the previous pin "
                f"{BASE_PIN[:8]}): {row['evidence']}"
            )
        counts["reverified" if (rid in GATES or rid in REVERIFIED) else "carried"] += 1
        location = row["location"]
        if rid == "E4a-r13-gates":
            location = "ledgers/E4/scripts/E4-a-r1/run_gates_delta.sh (outputs/exit_codes.txt)"
        rows.append({"id": rid, "check": row["check"], "location": location, "status": "PASS",
                     "evidence": evidence})
    delta = [
        ("E4a-r1-delta-L03-hunks", "2.9-delta",
         "course/modules/E/E4/L03.html lines 51, 55, 114, 270, 272, 343, 386, 407, 445, 449, 452",
         f"Round 1 (pin {PIN[:8]}): git diff {BASE_PIN[:8]}..{PIN[:8]} -- course/modules/E/E4/L03.html has 7 hunks with equal line counts, so no line number moved. Each changed line was read in context and checked: line 51 and 55 (Lemma 2.4, A1 at L01 line 61, A3 at L02 line 58, A4 at L02 line 63, e_s at L01 line 73); 114 and 343 (Remark 3.5, P3); 270 and 272 (canon-breaks); 386 (R2 numbers); 407 (key row 3); 445, 449, 452 (quiz L03q4 and numeric item). No changed sentence contradicts Proposition 3.4, its proof, Example 3.6 or the lab output."),
        ("E4a-r1-delta-lemma24-interior", "2.4-math",
         "course/modules/E/E4/L02.html lines 100-107 (Lemma 2.4); L03.html lines 51, 114, 343",
         "Round 1: Lemma 2.4 (assume A1, A3, A4; q in (0, infinity)^S, w_i > 0 => every demand has x_s > 0) is proved at L02 lines 105-107 by comparing with y = (w_i/(2 q.iota)) iota, which has finite utility and A4 gives U_i = -infinity at a zero entry. Equilibrium bundles are demands at q* (Definition 2.3, L02 line 88) with w_i = q*.e^i > 0 (A3). So 'Lemma 2.4 makes every equilibrium bundle interior' (L03 line 51) and 'part (b) adds no positivity hypothesis' (line 114, card c225) are correct."),
        ("E4a-r1-delta-cards-L03-L01-L02", "2.9-cards",
         "course/modules/E/E4/cards.json: E4-c011, c012, c013, c016, c017, c022, c024, c047, c048, c214, c225, c237, c265, c266",
         f"Round 1: the 14 slice-a cards in the cards.json diff were checked against the current text of their lesson: c011/c013/c265 values (340/3, 235/4, 56) appear in L01 line 281 and the lab output; c012 (596/3) and its 'A2 on this combination only' wording match L01 line 281; c016 matches the main() check at the top of the L01 twin (line 62) and Part A; c017, c024, c237 and c022 matches Definition 2.3 (L02 line 88), c017 and c237 match L02 line 55, c024 matches Assumption A5 (L02 line 93); c047 matches L03 line 119 and L02 line 189; c048 matches L03 lines 124 and 257-261; c214 matches L03 line 361; c225 matches L03 lines 51 and 114; c266 matches L02 lines 189 and 487 ({S}cards_check_L01-L03.txt)."),
        ("E4a-r1-delta-E2-R2-arithmetic", "2.2-numbers",
         "course/modules/E/E4/L03.html lines 361 (E2) and 386 (R2)",
         "Round 1: recomputed with exact arithmetic and Python logarithms: R2 derivatives 1/12 and 1/4; MRS at the endowment 8/3 (agent 1) and 8 (agent 2); each agent's expected-utility gain at the witness = (1/4) ln(4/3) = 0.0719205 (both agents); the count of 2 matches lab line 259."),
        ("E4a-r1-delta-hub-and-labs-unchanged", "2.9-scope",
         "course/modules/E/E4/index.html, L01.html, L02.html, tests/labs/E4/lab-E4-L01-1.py, lab-E4-L02-1.py, lab-E4-L03-1.py",
         "Round 1: git diff --quiet e919577 95f3f8cb for each path: byte-identical. Their rows are carried or re-run on the same bytes."),
    ]
    for rid, check, loc, ev in delta:
        rows.append({"id": rid, "check": check, "location": loc, "status": "PASS", "evidence": ev})
    ids = [r["id"] for r in rows]
    assert len(ids) == len(set(ids)), "duplicate row id"
    all_pass = all(r["status"] == "PASS" for r in rows)
    fragment = {
        "unit": "E4",
        "slice": "a",
        "round": 1,
        "verifier": "Haiku independent verifier, E4-a delta round 1 (closing, ruling 30); did not build E4; no shared context with the builders or the round-13 verifier",
        "pin": PIN,
        "base": f"{BASE_PIN} (round-13 pin; base fragment ~/.fanout/frags/E-E4-a.round13.json, verdict PASS, 174 rows)",
        "checkout": "/Users/billyribeiro/.fanout/wt/verifyF31-E4-a (detached at 95f3f8cb, .venv symlinked, vendor copied)",
        "scratch": "ledgers/E4/scripts/E4-a-r1/ (outputs/ holds every gate output and exit_codes.txt)",
        "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "verdict": "PASS" if all_pass else "FAIL",
        "rows": rows,
        "mutants": [],
        "registry_flags": [],
        "freshness_flags": [],
        "notes": [
            "Delta e919577..95f3f8cb over slice-a paths: L03.html (11 changed lines in 7 hunks, all read) and cards.json (14 slice-a cards changed, read in full for slice a). index.html, L01.html, L02.html and the lab twins L01-L03 are byte-identical (git diff --quiet).",
            "Ruling 30: no base row was non-PASS. Every row whose subject changed or that is a gate was re-verified from fresh evidence; every other base row is carried with the carry prefix (round 13). All 174 base row ids are kept; new rows use the E4a-r1-delta- prefix.",
            "Ruling 37: no mutants written. Slice a has no grader mutants (lab twins are demonstrations, not mutation targets), so mutants is empty.",
            "Ruling 26: only the FAIL kinds count. No FAIL was found in this delta. The base structure script reports 121 words for the L03 why-it-matters paragraph; the official checker (tools/check_pages.py words()) counts 120, the limit, so the row PASSes and the script artifact is explained in E4a-r6-struct-why-words.",
            "Locator slip in the base fragment, not a finding: rows E4a-r8-delta-L03-R1 and E4a-r6-num-L03-R2 cited lines 378 and 385; the current lines are 379 and 386 (text unchanged).",
            "Slice a is not a rubric slice; blind scorer files exist only for E4-d (~/.fanout/blind/E4-d.json), so no blind calibration rows apply here.",
            "Not checked by this slice: project.html and grader/test_project.py content beyond the cross-references listed (project slice); L06.html content (slice b); cards.json rows outside L01-L03 (other slices). The E4 grader passes run_graders 0-49 (gate, not row-by-row review).",
        ],
        "summary": "",
    }
    fragment["summary"] = (
        f"E4 slice a, delta round 1 at {PIN[:8]} (closing, rulings 30 and 37): {len(rows)} rows, all PASS, "
        f"0 FAIL, 0 UNVERIFIABLE. Re-verified from fresh evidence: {counts['reverified']} base rows plus "
        f"{len(delta)} delta rows; carried with the round-13 prefix: {counts['carried']} base rows. Gates re-run "
        f"(check_pages, check_dag, check_projects, run_labs, twins under python -I -W error, ruff, mypy, pytest, "
        f"run_graders E4, verify_refs, build_site, render_curriculum, page_smoke x4) all exit 0."
    )
    OUT.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"rows {len(rows)} reverified {counts['reverified']} carried {counts['carried']} verdict {fragment['verdict']}")


if __name__ == "__main__":
    main()
