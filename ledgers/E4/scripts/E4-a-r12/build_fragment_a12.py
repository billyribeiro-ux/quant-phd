"""E4 slice a, round 12: writes ledgers/E4/E4-a.json from the round-11 fragment's row ids and this round's evidence.

Every round-11 row id is kept. Delta since the round-11 pin 11d7077 (git diff 11d7077 5db69a9, slice-a paths): index.html
line 63; L01.html lines 51, 104, 253-254, 280; L02.html lines 51, 568; L03.html line 361; tests/labs/E4/lab-E4-L01-1.py
lines 93-94; plans/FINAL-ARCHITECT-RULINGS.md item 13 (grading of worked values). A row is carried only when every cited
line and file is byte-identical to the round-11 pin; every other row is re-verified in this round.
Run from the checkout root: .venv/bin/python -I ledgers/E4/scripts/E4-a-r12/build_fragment_a12.py
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PREV = Path("/Users/billyribeiro/.fanout/frags/E-E4-a.round11.json")
OUT = ROOT / "ledgers/E4/E4-a.json"
SCR = "ledgers/E4/scripts/E4-a-r12"
OUTS = f"{SCR}/outputs"
PIN = "5db69a9bee460736c318ebfacc7200ee5a6eb0f0"
PREV_PIN = "11d7077a290f7960b183d3a5a6631af4773888f9"

prev = json.loads(PREV.read_text(encoding="utf-8"))
prev_rows = {r["id"]: r for r in prev["rows"]}

CARRY_NOTE = "Carried from round 11 ({files} byte-identical since the previous pin {pin}): "

# Round-11 rows whose cited lines and files are byte-identical in this delta: id -> cited files and lines.
CARRY: dict[str, str] = {
    "E4a-r6-hours-arith": "index.html lines 29, 41, 43, 139; L01 to L03 line 2",
    "E4a-r6-hub-titles": "index.html lines 129-149; L01 to L09 h1 (index line 63 is the only changed index line and is not cited)",
    "E4a-r6-hub-unlocks": "index.html line 36",
    "E4a-r6-hub-prereq-titles": "index.html line 35",
    "E4a-r6-hub-placement": "index.html lines 66-135",
    "E4a-r6-hub-numbers": "index.html lines 7, 31, 33, 40-43, 68, 71-73, 113-120, 139",
    "E4a-r6-hub-objectives": "index.html lines 50-57",
    "E4a-r6-hub-card-claims-L01-03": "index.html lines 141-143",
    "E4a-r6-hub-forward-naming": "index.html lines 33, 53, 56, 139, 149",
    "E4a-r6-num-L01-M1-rounding": "L01.html line 322",
    "E4a-r6-num-L01-E3-rounding": "L01.html line 386",
    "E4a-r6-num-L02-example": "L02.html lines 124-126, 187-190, 299-363, 377-393, 429-443, 506-529",
    "E4a-r6-num-L02-remark26": "L02.html line 125",
    "E4a-r6-num-L02-misconceptions": "L02.html lines 358, 362, 366",
    "E4a-r6-num-L03-example36": "L03.html lines 119, 250-254, 303-304, 476",
    "E4a-r6-num-L03-R2": "L03.html line 385",
    "E4a-r6-math-L01-remark111": "L01.html line 155",
    "E4a-r6-math-L01-R1-countable": "L01.html lines 287, 394-399",
    "E4a-r6-math-L01-R2-R3-P": "L01.html lines 345-411",
    "E4a-r6-math-L02-lemma-prop25": "L02.html lines 99-121",
    "E4a-r6-math-L02-cor27-prop28": "L02.html lines 128-161",
    "E4a-r6-math-L02-KKT-paragraph": "L02.html line 164",
    "E4a-r6-math-L02-prop29-remark210": "L02.html lines 168-185",
    "E4a-r6-math-L02-R1-R3-P-M": "L02.html lines 404-470",
    "E4a-r6-math-L03-def33": "L03.html lines 67-74",
    "E4a-r6-math-L03-prop34a": "L03.html lines 91-101",
    "E4a-r6-math-L03-prop34b": "L03.html lines 103-110",
    "E4a-r6-math-L03-remark35-P3": "L03.html lines 113-115, 339-343",
    "E4a-r6-math-L03-R1-free-disposal": "L03.html lines 375-379",
    "E4a-r6-math-L03-R3": "L03.html lines 389-393",
    "E4a-r6-lab-L02-hypothesis": "L02.html line 194 and the expected block lines 315-339; twin tests/labs/E4/lab-E4-L02-1.py",
    "E4a-r6-lab-L02-interpretation": "L02.html line 340",
    "E4a-r6-lab-L02-code": "L02.html lines 195-314; twin tests/labs/E4/lab-E4-L02-1.py",
    "E4a-r6-lab-L03-hypothesis": "L03.html line 124 and the expected block lines 250-260",
    "E4a-r6-lab-L03-interpretation": "L03.html line 261",
    "E4a-r6-lab-L03-code": "L03.html lines 125-249; twin tests/labs/E4/lab-E4-L03-1.py",
    "E4a-r6-quiz-hub": "index.html lines 66-135",
    "E4a-r6-quiz-L01": "L01.html lines 437-506",
    "E4a-r6-quiz-L03": "L03.html lines 418-487",
    "E4a-r6-hub-lede-and-ladder": "index.html lines 33, 155-161",
    "E4a-r6-observation-noise-e": "L02.html line 55",
    "E4a-r7-math-L03-R2-compensation": "L03.html line 385",
    "E4a-r7-data-simulated-labels": "twins tests/labs/E4/lab-E4-L06-1.py, lab-E4-L07-1.py, lab-E4-L08-1.py (not in the delta)",
    "E4a-r8-delta-index-lede": "index.html line 33",
    "E4a-r8-delta-index-data": "index.html lines 38 and 167",
    "E4a-r8-delta-L01-R1": "L01.html line 397",
    "E4a-r8-delta-L02-line55": "L02.html line 55",
    "E4a-r8-delta-L02-canon": "L02.html line 349",
    "E4a-r8-delta-L03-line55": "L03.html line 55",
    "E4a-r8-delta-L03-R1": "L03.html line 378",
    "E4a-r9-math-L01-def-1-2-probability": "L01.html line 67",
    "E4a-r9-prose-L02-meta-description": "L02.html line 7",
    "E4a-r9-structure-L03-canon-limits": "L03.html lines 264-273",
    "E4a-r10-delta-index-L38": "index.html line 38",
    "E4a-r10-delta-index-L167": "index.html line 167",
    "E4a-r10-delta-L01-L67": "L01.html line 67",
    "E4a-r10-delta-L01-L155": "L01.html line 155",
    "E4a-r10-delta-L01-L287": "L01.html line 287",
    "E4a-r10-delta-L01-L322": "L01.html line 322",
    "E4a-r10-delta-L01-R1": "L01.html lines 395-397",
    "E4a-r10-delta-L02-L7": "L02.html line 7",
    "E4a-r10-delta-L02-L348": "L02.html line 348",
    "E4a-r10-delta-L03-L270": "L03.html line 270",
    "E4a-r10-hub-quiz-skill": "index.html lines 116-133",
    "E4a-r11-delta-index-L50": "index.html line 50",
    "E4a-r11-delta-index-L141": "index.html line 141",
    "E4a-r11-delta-index-L38-parts": "index.html lines 38 and 167",
    "E4a-r11-delta-L01-L7": "L01.html line 7",
    "E4a-r11-delta-L01-L109": "L01.html line 109",
    "E4a-r11-delta-L02-L349": "L02.html line 349",
    "E4a-r11-hub-skill-rung1": "index.html lines 117 and 123",
    "E4a-r6-notation-e-collision": "L02.html line 55; L03.html lines 55, 105, 335",
    "E4a-r6-notation-mu-local": "L02.html line 164",
    "E4a-r7-notation-u-local": "L02.html lines 68-71; L03.html line 69; L06.html (noise supply u, not in the delta)",
    "E4a-r8-delta-L03-R2": "L03.html line 385",
}

# Round-11 rows re-verified in this round (their subject changed or was re-run). Status and evidence are this round's.
REVERIFY: dict[str, tuple[str, str]] = {
    "E4a-r6-cmd-check_pages": ("PASS", f"Re-run this round: `.venv/bin/python tools/check_pages.py --unit E4` exit 0, 'check_pages E4: PASS' ({OUTS}/check_pages_E4.txt; run_commands.sh)."),
    "E4a-r6-cmd-check_dag": ("PASS", f"Re-run: `tools/check_dag.py --all` exit 0, every unit including E4 'PASS' ({OUTS}/check_dag_all.txt)."),
    "E4a-r6-cmd-run_labs": ("PASS", f"Re-run: `tools/run_labs.py --unit E4` 'run_labs E4: PASS (12/12)'; `--page L01`, `--page L02`, `--page L03` each exit 0 ({OUTS}/run_labs_*.txt)."),
    "E4a-r6-cmd-page_smoke": ("PASS", f"Re-run alone per page: `tools/page_smoke.py --unit E4 --pages index`, `--pages L01`, `--pages L02`, `--pages L03`: each 'page_smoke ...: PASS', exit 0 ({OUTS}/page_smoke_*.txt)."),
    "E4a-r6-cmd-twins-alone": ("PASS", f"Each twin run alone: `.venv/bin/python -I -W error tests/labs/E4/lab-E4-L0n-1.py` rc 0 for L01, L02, L03 (CPython 3.14.8), stderr empty; checked by {SCR}/lab_page_twin_check.py ('FAILS: 0', {OUTS}/lab_page_twin_check.txt)."),
    "E4a-r6-cmd-twin-embed": ("PASS", f"{SCR}/lab_page_twin_check.py re-run: data-run text equals the twin source (trailing newline only) and pre.expected equals stdout for L01, L02, L03 ({OUTS}/lab_page_twin_check.txt)."),
    "E4a-r6-cmd-ruff": ("PASS", f"`.venv/bin/python -m ruff check tests/labs/E4 course/modules/E/E4/grader`: 'All checks passed!'; `ruff format --check tests/labs/E4`: '12 files already formatted' ({OUTS}/ruff_slice.txt, ruff_format.txt)."),
    "E4a-r6-cmd-mypy": ("PASS", f"`.venv/bin/python -m mypy --no-incremental tests/labs/E4`: 'Success: no issues found in 12 source files' ({OUTS}/mypy_labs.txt)."),
    "E4a-r6-cmd-pytest": ("PASS", "`.venv/bin/python -m pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py`: every test passed (run twice this round; the second run printed only dots and the summary line)."),
    "E4a-r6-cmd-verify_refs": ("PASS", f"`tools/verify_refs.py --offline` over the whole registry: 'offline integrity: 560 entries, 0 problems', exit 0 ({OUTS}/verify_refs_offline.txt). The live Crossref run was not executed (network); the slice cites no registry key (no data-cite or data-locator in index, L01 to L03; the data-references lists are empty), so there is no entry for it to resolve."),
    "E4a-r6-cmd-check_projects": ("PASS", f"Re-run: `tools/check_projects.py --unit E4`: 'check_projects E4: PASS' (cross-slice, project page is slice e's; {OUTS}/check_projects_E4.txt)."),
    "E4a-r11-cmd-verify_refs-offline": ("PASS", f"Re-run: `tools/verify_refs.py --offline`, 560 entries, 0 problems, exit 0 ({OUTS}/verify_refs_offline.txt)."),
    "E4a-r10-cmd-run_graders": ("PASS", f"Re-run: `tools/run_graders.py --unit E4 --seeds 0-49`: 'run_graders E4: PASS (reference 50/50 seeds)', exit 0 ({OUTS}/run_graders.txt; cross-slice, grader unchanged)."),
    "E4a-r6-struct-lesson-order": ("PASS", f"{SCR}/structure_slice_a.py (archived {OUTS}/structure.out): section order of index, L01 to L03 lab-before-canon-breaks, misconceptions, problem set, key results, quiz, references as in BUILDER_RULES 4.2; FAILS 0."),
    "E4a-r6-struct-counts": ("PASS", f"{SCR}/structure_slice_a.py: quiz 9 items on each lesson (8 to 15 required); misconceptions 3 each; 3 problems in each of Mechanics, Proof, Empirical, Research on L01, L02, L03 ({OUTS}/structure.out)."),
    "E4a-r6-struct-why-words": ("PASS", f"{SCR}/structure_slice_a.py: why-it-matters words L01 114, L02 118, L03 120 (limit 120). L01 rose from 108 to 114 with the delta's Proposition 1.4 and Definition 1.6 references; still within the limit ({OUTS}/structure.out)."),
    "E4a-r6-struct-solution-words": ("PASS", f"{SCR}/structure_slice_a.py: every details.solution block at least 15 words on L01 to L03 ({OUTS}/structure.out)."),
    "E4a-r10-structure-script": ("PASS", f"{SCR}/structure_slice_a.py re-run: 168 PASS, FAILS 0 (counts, word limits, tiers, quiz, dfn owners, links) ({OUTS}/structure.out)."),
    "E4a-r11-cmd-structure-script": ("PASS", f"Same run as above: `.venv/bin/python -I ledgers/E4/scripts/E4-a-r12/structure_slice_a.py` exit 0, FAILS 0."),
    "E4a-r6-dag-closure": ("PASS", f"`tools/check_dag.py --all` PASS; {SCR}/structure_slice_a.py: concept links resolve to ids in course/concepts.html or to a def in an earlier lesson ({OUTS}/structure.out)."),
    "E4a-r6-dag-defs-unique": ("PASS", f"{SCR}/structure_slice_a.py dfn owners: arrow-debreu-security L01, arrow-debreu-equilibrium L02, first-welfare-theorem L03; each defined once with dfn id = def-<data-concept>."),
    "E4a-r8-concept-anchors-owners": ("PASS", f"{SCR}/supplementary_scans.py (6): every hub concept link in index.html is used by a lesson (L01 to L09 data-concept); check_dag PASS ({OUTS}/supplementary.out)."),
    "E4a-r6-hub-KKT-claim": ("PASS", "index.html line 63 (changed by the delta; the M7 sentence is unchanged): 'From M7 it uses Lagrange multipliers and the KKT conditions'; L02.html line 164 uses the KKT conditions."),
    "E4a-r6-hub-prereq-usage": ("PASS", f"{SCR}/supplementary_scans.py (6): each hub concept link (index line 63 after the delta) has a data-concept use in L01 to L09 ({OUTS}/supplementary.out)."),
    "E4a-r6-data-none": ("PASS", f"index lines 38 and 167 say no dataset; {SCR}/supplementary_scans.py (4): no open(, urllib, requests, socket or http in the three twins; no data-files attribute on the lab sections."),
    "E4a-r6-dag-D-terms": ("PASS", f"{SCR}/supplementary_scans.py (2): none of 'state price', 'stochastic discount', 'martingale', 'Bayes', 'Banach', 'intermediate value', 'two-fund', 'determinacy', 'efficient markets', 'Kyle', 'common knowledge', 'noise-trader risk', 'diagnostic expectations', 'probability of informed trading' in visible text of index, L01 to L03. The index AP1 unlock title 'Stochastic Discount Factor' (index line 36) is the curriculum module title, a name and not a use ({OUTS}/supplementary.out)."),
    "E4a-r6-notation-macros": ("PASS", f"{SCR}/supplementary_scans.py (1): every macro in index and L01 to L03 math is standard or registered (\\E, \\Prob, \\R in notation/notation.json; INFO list in {OUTS}/supplementary.out); structure_slice_a.py: no TeX control word outside the notation set."),
    "E4a-r6-notation-registered-symbols": ("PASS", f"{SCR}/supplementary_scans.py (1): no \\mathbb{{E}}, \\mathbb{{R}}, \\mathbb{{Q}}, \\Phi, \\ast, R_f in math; supplementary_scans.py (8) finds no bare T symbol in index or L01 to L03 math ({OUTS}/supplementary.out)."),
    "E4a-r8-macros-and-symbols": ("PASS", f"{SCR}/supplementary_scans.py (1) and the bare-T regex scan above: the registered macros and symbols are used with their registered meanings; no forbidden symbol."),
    "E4a-r10-scan-notation": ("PASS", f"{SCR}/supplementary_scans.py (1): no forbidden symbol; every macro standard or registered ({OUTS}/supplementary.out)."),
    "E4a-r6-banned-phrases": ("PASS", f"{SCR}/banned_scan.py: BANNED and PROCESS lists (TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly; verifier, builder, build, round, REQUESTS, unit report, fixer, ledger): 0 hits in index, L01 to L03 visible text ({OUTS}/banned_scan.txt)."),
    "E4a-r6-process-words": ("PASS", f"{SCR}/banned_scan.py: 0 process-word hits in index and L01 to L03 visible text; grep of the three twins for verifier, builder, round, planner: only 'rounding' (ordinary word, L02 twin line 6)."),
    "E4a-r10-ellipsis": ("PASS", f"{SCR}/banned_scan.py: 0 ellipsis hits in index and L01 to L03 visible text (outside code)."),
    "E4a-r6-scope-words": ("PASS", "Re-read this round: L01 line 51 'every claim ... is a weighted sum' (Proposition 1.4, A1 finite); L02 line 51 'any positive price vector at which each agent has a demand' (Proposition 2.5 hypothesis); L03 line 51 and Proposition 3.4 hypotheses A1, A3, A4. Each universal word has its proof or stated hypothesis."),
    "E4a-r6-define-before-use": ("PASS", "Re-read this round. The new L01 line 51 cites Proposition 1.4 and Definition 1.6 in the why-it-matters paragraph, as the round-11 text already cited Definitions 1.2 and 1.3 there; introductory numbered cross-references are the precedent, and no term is used in a body section before its definition (Definition 1.6 at L01 line 108; Definition 2.3 at L02 line 88; Definition 3.1 to 3.3 at L03 lines 58, 63, 68)."),
    "E4a-r6-attribution": ("PASS", f"{SCR}/supplementary_scans.py (3): no four-digit year in visible text of index, L01 to L03; no bibliographic record in the slice ({OUTS}/supplementary.out)."),
    "E4a-r6-num-L01-remaining": ("PASS", f"Re-derived this round: {SCR}/rederive_slice_a12.py (61 PASS, FAILS 0; {OUTS}/rederive.out): 340/3, 56, 596/3, 235/4, 9/8, 55/3, 35/6, 25/2, 340/3 to 113.33, 58.75, 2*340/3 identities; the changed line 280 (overweight) matches the twin output."),
    "E4a-r6-num-L03-grid": ("PASS", f"Re-derived by {SCR}/rederive_slice_a12.py: 125 allocations, 0 improvements of the equilibrium, 2 of the endowment, first at (2,4,3)/(2,4,1) with TOL 1e-12, plus a 13-point-per-state finer grid giving 0 at the equilibrium ({OUTS}/rederive.out)."),
    "E4a-r8-grid-recount": ("PASS", f"Same run as E4a-r6-num-L03-grid: {SCR}/rederive_slice_a12.py; lab output lines 8-11 of the L03 twin run."),
    "E4a-r7-rederive-all-numbers": ("PASS", f"{SCR}/rederive_slice_a12.py (61 PASS) and the structure scan: every number in index, L01 to L03 prose re-derived or read against a lab expected block ({OUTS}/rederive.out)."),
    "E4a-r8-rederive-numbers": ("PASS", f"{SCR}/rederive_slice_a12.py: 61 PASS, FAILS 0 (all numbers of Examples 1.5, 2.11, 3.6, Remark 2.6, the problem solutions and the lab hypotheses) ({OUTS}/rederive.out)."),
    "E4a-r6-math-L01-props": ("PASS", "L01 lines 77-151 re-read this round: Proposition 1.4 (A1), Proposition 1.7 (A1, A2), Proposition 1.8 (proof takes x = e_s), Proposition 1.10 (both directions in the proof). Proof steps follow from the stated assumptions; {SCR}/rederive_slice_a12.py checks the instances."),
    "E4a-r6-math-L01-A2-sentence": ("PASS", "L01 line 104 (changed by the delta): 'A2 excludes quantity discounts, bid-ask spreads and price impact. Each of them makes V depend on the size or the direction of a trade, so V need not be linear.' Quantity discounts and price impact depend on size; bid-ask depends on direction (buy at ask, sell at bid); the 'need not be linear' conclusion is the hedged one the text states."),
    "E4a-r6-math-L03-M-P-E": ("PASS", f"L03 lines 300-369 re-read; M1 (MRS 2), M2 (x = (3/2, 3), MRS 2), M3 (feasible split), P1, P2 (MRS identity), P3 (hypotheses) checked; E2 (line 361, changed) re-verified below; {SCR}/rederive_slice_a12.py covers the numbers."),
    "E4a-r6-lab-L01-hypothesis": ("PASS", f"L01 line 160 hypothesis vs the twin run this round ({OUTS}/lab_page_twin_check.txt; output at /tmp/e4-v-a12-L01.out): coefficients 100, 40, 0, 250; value 340/3 and 56; linearity with weights 2, -1/2; expected payoff 235/4; negative and 9/8-sum vectors rejected with ValueError. Every printed value matches."),
    "E4a-r6-lab-L01-interpretation": ("PASS", "L01 line 281 re-read this round: Part A exact decomposition; Part B 340/3 and 56; Part C linearity for one combination (weights 2 and -1/2); Part D False flag; Part E two rejection messages. It names no printed line the lab does not print; the 'short' label of round 11 is now 'overweight' in both the twin and the expected block."),
    "E4a-r6-lab-L01-code": ("PASS", f"L01 page code equals tests/labs/E4/lab-E4-L01-1.py (trailing newline only), checked this round by {SCR}/lab_page_twin_check.py; the twin changed at lines 93-94 (variable and label renamed) and the page follows it."),
    "E4a-r6-lab-page-equals-twin": ("PASS", f"{SCR}/lab_page_twin_check.py (this round): for L01, L02, L03 the data-run text equals the twin and pre.expected equals the stdout of `python -I -W error` ({OUTS}/lab_page_twin_check.txt)."),
    "E4a-r6-lab-hypothesis-before-output": ("PASS", f"{SCR}/lab_page_twin_check.py this round: the hypothesis paragraph precedes the code block and the interpretation follows the expected block for L01, L02, L03 ({OUTS}/lab_page_twin_check.txt)."),
    "E4a-r6-lab-stdlib-no-network": ("PASS", f"{SCR}/supplementary_scans.py (4): the three twins import only __future__, fractions, math, itertools; no file, network or socket access ({OUTS}/supplementary.out)."),
    "E4a-r6-lab-main-toplevel": ("PASS", f"{SCR}/supplementary_scans.py (5): each twin ends with an unconditional top-level main() call and has no __main__ guard ({OUTS}/supplementary.out)."),
    "E4a-r6-lab-runtime": ("PASS", f"page_smoke re-run alone for L01, L02, L03 this round: lab timings 0.0 s each (well under 10 s); {OUTS}/page_smoke_L0*.txt."),
    "E4a-r6-lab-no-mutants": ("PASS", "Lab twins are demonstrations; mutation testing applies to the project grader only (plan ruling). Slice a has no grader and no mutants list."),
    "E4a-r6-quiz-L02": ("PASS", "L02 quiz lines 497-570 re-read this round, all 9 items: answers (pi_s w/q_s; 2; q.z = 0 with 'unweighted sum not implied'; Lemma 2.4 reason; 1/8; theta_i; invariance under psi; Definition 2.2; Proposition 2.9 reading). Item 9's explanation now reads '(§4)' (line 568), which is correct: the construction is Proposition 2.9 in §4."),
    "E4a-r7-hub-cross-unit-titles": ("PASS", "index.html line 63 (changed): 'adverse selection' matches E2 L03 h1 'Adverse Selection' (course/modules/E/E2/L03.html line 35); E3 index h1 'Decision Theory Under Risk & Ambiguity' matches the hub's E3 title; M7 'Optimization' unchanged."),
    "E4a-r7-delta-coverage": ("PASS", f"git diff --name-only 11d7077 5db69a9 restricted to the slice paths: index.html, L01.html, L02.html, L03.html, tests/labs/E4/lab-E4-L01-1.py; every changed hunk read (git diff -U0 hunks at index 63; L01 51, 104, 253-254, 280; L02 51, 568; L03 361; twin 93-94). Curriculum, tools, notation and references are not in the delta (the curriculum change is in 02-economics-finance-core.yaml line 428, not an E4 item)."),
    "E4a-r8-delta-L03-E2": ("PASS", "L03 line 361 (changed by the delta) re-read: the conclusion 'rests on the hand witness of Problem R2, not on the count'; the first witness (2,4,3)/(2,4,1) sums to (4,8,4); each agent gains (1/4) ln(4/3) (exact: agent 1 (1/2) ln(2/3) + (1/4) ln 3 = (1/4) ln(4/3); agent 2 (1/2) ln 2 + (1/4) ln(1/3) = (1/4) ln(4/3)); Problem R2 line 386 gives the explicit trade. All verified this round."),
    "E4a-r8-data-labs-simulated-labels": ("PASS", f"{SCR}/supplementary_scans.py (5): no random draws in lab-E4-L01-1, L02-1, L03-1; grep this round: `random.` calls appear only in lab-E4-L06-1, L07-1, L08-1 (the seeded simulations); L04, L05, L09 twins make no random call; index lines 38 and 167 state the SIMULATED labels."),
    "E4a-r8-page-smoke-no-external": ("PASS", f"page_smoke re-run alone for index, L01, L02, L03 this round: each PASS, zero console errors and no external request reported ({OUTS}/page_smoke_index.txt, page_smoke_L0*.txt)."),
    "E4a-r11-delta-index-L63": ("PASS", "index.html line 63 re-read this round: the M3 sentence 'From M3 it uses linear maps and vector spaces' is present; the sentence changed by the delta (adverse selection) is verified in E4a-r12-delta-index-L63."),
    "E4a-r11-delta-L03-L361": ("PASS", "L03 line 361 re-read this round against Problem R2 (line 386) and the numbers in E4a-r8-delta-L03-E2; PASS for the current text."),
    "E4a-r11-delta-L02-L568": ("PASS", "FIXED in 5db69a9: L02.html line 568 now reads '(§4)'. §4 'An equilibrium in closed form' holds Proposition 2.9 (line 169), the construction the explanation names. Verified this round."),
    "E4a-r11-lab-L01-partE-label": ("PASS", "FIXED in 5db69a9: tests/labs/E4/lab-E4-L01-1.py lines 93-94 use 'overweight' (entries sum to 9/8, which is correct) and the expected block (L01.html line 280) reads 'rejected overweight message state probabilities must sum to 1'. The page block equals the twin output (lab_page_twin_check PASS this round)."),
    "E4a-r6-references-none": ("PASS", f"Re-run this round: grep -c 'data-cite|data-locator' gives 0 for index.html, L01.html, L02.html, L03.html (no registry citation); each lesson has one empty '<ol data-references></ol>' (L01 line 512, L02 line 576, L03 line 494); sections 9/10/8 say the lesson cites no registry source."),
    "E4a-r10-rederive-script": ("PASS", f"{SCR}/rederive_slice_a12.py re-run: 61 PASS, FAILS 0 ({OUTS}/rederive.out), covering the numbers of index, L01 to L03 prose and exercises."),
    "E4a-r10-embed": ("PASS", f"{SCR}/lab_page_twin_check.py re-run this round: L01, L02, L03 page blocks equal their twins and expected blocks equal twin output ({OUTS}/lab_page_twin_check.txt)."),
}

# Rows that are FAIL in this round, with their fixes.
FAIL_ROWS = [
    {
        "id": "E4a-r12-ruling13-L01-keyrow5",
        "check": "2.3-grades (FINAL-ARCHITECT-RULINGS item 13, T versus C for worked values)",
        "location": "course/modules/E/E4/L01.html line 427 (section 7 key results, row 5)",
        "status": "FAIL",
        "evidence": (
            "Row 5 grades 'The four-state values 340/3 and 56 cents, the linearity check, and the expected payoff 235/4 cents' as T, "
            "source 'Exact arithmetic of Proposition 1.7; reproduced by Lab 1, Parts B to D'. Ruling 13 (plans/FINAL-ARCHITECT-RULINGS.md, "
            "added in 5db69a9, item 13): a value the page derives by hand in a numbered Example is T with the Example as basis; a value "
            "that appears only in lab output is C naming the lab. Example 1.5 (L01 line 93) derives only the decomposition. The prices "
            "(1/2, 1/3, 1/4, 1/5) appear only in the Lab 1 hypothesis (line 160) and in the twin (tests/labs/E4/lab-E4-L01-1.py lines 24-26, "
            "79-89); the values 340/3, 56, 596/3 and 235/4 are printed by the twin (run this round: 'value_of_claim 340/3 value_of_other 56', "
            "'value_of_combination 596/3', 'expected_payoff_claim 235/4') and quoted in lines 281, 303, 379, 386. No numbered Example or proof "
            "derives them by hand. Verified by /rederive_slice_a12.py (values recomputed, 61 PASS) and by reading L01 lines 91-95 and 136-160."
        ),
        "fix": (
            "Either (a) regrade row 5 to C with basis 'Lab 1, Parts B to D (exact Fraction arithmetic; the prices are lab inputs and no "
            "numbered Example derives these values)', and change the row 5 source to match; or (b) add a numbered Example in §1 or §3 that "
            "derives 340/3, 56 and 235/4 by hand from the stated prices and probabilities, and grade that row T with the Example as basis. "
            "Either way, L01 line 511 (references paragraph, see E4a-r8-delta-L01-references) and the card E4-c011 to E4-c013 in cards.json "
            "(slice F, out of this slice) must carry the same grade and basis."
        ),
    },
    {
        "id": "E4a-r12-ruling13-L02-keyrow6",
        "check": "2.3-grades (FINAL-ARCHITECT-RULINGS item 13)",
        "location": "course/modules/E/E4/L02.html line 487 (section 8 key results, row 6); line 575 (references paragraph)",
        "status": "FAIL",
        "evidence": (
            "Row 6 grades 'The example values of Example 2.11 and the residuals of Lab 2' as T with source 'Exact arithmetic from Proposition 2.9; "
            "reproduced by Lab 2, Parts B to E'. Two different kinds of value are mixed. (i) The Example 2.11 values (theta 9/16 and 7/16 derived by "
            "hand on L02 line 189; prices (1/8, 1/32, 1/16) and bundles stated from the same formulas) are derived in a numbered Example, so ruling 13 "
            "requires T with the Example as basis, but the row names Proposition 2.9 as its basis. (ii) The residuals (budget, market clearing and "
            "Walras, all 0) appear only in Lab 2 output (Part C; the lab's interpretation line 340 says it 'verifies these identities for one economy'). "
            "Ruling 13 makes them C naming Lab 2. Checked this round: the Example arithmetic re-derived (rederive_slice_a12.py, PASS); the residual values "
            "printed by the twin: 'agent 1 budget_residual 0', 'state 0 market_clearing_residual 0', 'walras_law_residual 0' (all zero)."
        ),
        "fix": (
            "Split row 6 into two rows: (a) 'Example 2.11 values (theta, prices, equilibrium bundles)', grade T, basis 'Example 2.11 (theta by hand) "
            "with Proposition 2.9'; (b) 'Budget, market-clearing and Walras residuals of Lab 2 are zero', grade C, basis 'Lab 2, Parts C and E (exact "
            "Fraction arithmetic)'. Change the references paragraph (line 575) so it says that a lab-only check is graded C, not T. Cards E4-c031 to "
            "E4-c035 (cards.json, slice F) must carry the same grades and bases."
        ),
    },
    {
        "id": "E4a-r8-delta-L01-references",
        "check": "2.9-prose (grade statement consistent with the table)",
        "location": "course/modules/E/E4/L01.html line 511 (section 9 references paragraph)",
        "status": "FAIL",
        "evidence": (
            "Line 511 reads 'Each graded result in the table of §7 is proved on this page (grade T) from Definitions 1.1 to 1.9 and the assumptions "
            "A1 and A2, and Lab 1, Parts B to D, reproduces its exact values 340/3, 56, 596/3 ...'. Row 5 of that table is a lab-printed value that "
            "is not proved on this page (see E4a-r12-ruling13-L01-keyrow5), so the sentence is false as written once row 5 is graded as ruling 13 requires."
        ),
        "fix": (
            "After the row 5 fix, rewrite line 511 to state that each T result in the table of §7 is proved on this page, and that the four-state values "
            "are C results reproduced by Lab 1, Parts B to D (or, if a numbered Example derives them, that they are T with that Example as basis)."
        ),
    },
    {
        "id": "E4a-r6-math-keyresults",
        "check": "2.3-grades (key-results tables)",
        "location": "L01 section 7 (line 427, row 5); L02 section 8 (line 487, row 6); L03 section 6 (lines 405-409)",
        "status": "FAIL",
        "evidence": (
            "The round-11 PASS was given under the earlier grading rule. Under ruling 13 (added in 5db69a9), L01 row 5 and L02 row 6 are wrong in grade and basis "
            "(E4a-r12-ruling13-L01-keyrow5, E4a-r12-ruling13-L02-keyrow6). The L01 rows 1 to 4 (Propositions 1.4, 1.7, 1.8, 1.10, T with proofs in §2 and §3) "
            "and the L02 rows 1 to 5 (Lemma 2.4, Proposition 2.5, Corollary 2.7, Proposition 2.8, Proposition 2.9, T with proofs) pass. L03 rows 1 to 5 pass: "
            "row 3 is T with 'Derived in Example 3.6' (the Example derives the three MRS values by hand, ruling 13), and row 5 is C with basis Lab 3 Part B "
            "(the 125-point grid, a finite enumeration)."
        ),
        "fix": "Apply the two fixes in E4a-r12-ruling13-L01-keyrow5 and E4a-r12-ruling13-L02-keyrow6; the L03 table needs no change.",
    },
    {
        "id": "E4a-r6-grades-claims",
        "check": "2.3-grades (claim spans)",
        "location": "L01 line 427 (key-results row 5); L02 line 487 (row 6); index and L01 to L03 claim spans",
        "status": "FAIL",
        "evidence": (
            "Claim spans re-read this round. The theorem, proposition, lemma and corollary blocks are T with proofs (L01 lines 78, 113, 127, 142; L02 lines 100, 110, "
            "128, 143, 169; L03 lines 81) and pass. The round-11 claim 'the lab exact results T (L01 line 427)' is the defect of ruling 13 (E4a-r12-ruling13-L01-keyrow5); "
            "the same applies to L02 line 487 (E4a-r12-ruling13-L02-keyrow6)."
        ),
        "fix": "Apply the two key-results fixes; re-grade the lab-only values as C naming the lab (see the two rows named above).",
    },
]

# New rows for this round's delta and checks, all PASS unless listed in FAIL_ROWS.
NEW_ROWS = [
    {
        "id": "E4a-r12-delta-L01-L51",
        "check": "2.9-prose / 2.4-math (delta)",
        "location": "L01.html line 51 (why-it-matters)",
        "status": "PASS",
        "evidence": "Re-read: 'proves that every claim (Definition 1.2) is a weighted sum of these securities (Proposition 1.4, under A1)'. Proposition 1.4 begins 'Assume A1' (L01 line 78). 'the sum of security prices (Definition 1.6) times payoffs' - Definition 1.6 (line 108) defines the security price vector; the value formula is Proposition 1.7 (line 113), which the sentence states without a number. Word count 114 (structure script).",
    },
    {
        "id": "E4a-r12-delta-L01-L104",
        "check": "2.4-math (delta)",
        "location": "L01.html line 104 (Assumption A2 explanation)",
        "status": "PASS",
        "evidence": "Re-read: 'Each of them makes V depend on the size or the direction of a trade, so V need not be linear.' Quantity discounts and price impact depend on size; a bid-ask spread depends on the direction of the trade. The hedged 'need not be linear' is the claim the text supports, and A2 itself is left as an assumption ('this lesson does not derive it').",
    },
    {
        "id": "E4a-r12-delta-L01-partE",
        "check": "2.5-labs (delta, round-11 FAIL fixed)",
        "location": "tests/labs/E4/lab-E4-L01-1.py lines 93-94; course/modules/E/E4/L01.html lines 253-254 and 280",
        "status": "PASS",
        "evidence": f"Part E vector (1/8, 3/8, 3/8, 1/4) sums to 9/8 (rederive_slice_a12.py PASS 'overweight vector sums to 9/8'); label 'overweight' is accurate. Page code equals twin (lab_page_twin_check PASS); expected line 280 equals the twin output line 19 ({OUTS}/lab_page_twin_check.txt). Module docstring line 12 ('do not sum to 1') matches.",
    },
    {
        "id": "E4a-r12-delta-L01-L280-281",
        "check": "2.5-labs (delta)",
        "location": "L01.html lines 280-281 (expected block, interpretation)",
        "status": "PASS",
        "evidence": "Expected block equals twin output (lab_page_twin_check PASS). Interpretation (line 281) 'Part E prints the two rejection messages' is true of the twin output lines 18-19; the Part D flag reads False (twin output line 16), matching the text.",
    },
    {
        "id": "E4a-r12-delta-L02-L51",
        "check": "2.4-math (delta)",
        "location": "L02.html line 51 (why-it-matters)",
        "status": "PASS",
        "evidence": "'under A1, A3 and A4, that the value of the excess demand (Definition 2.3) is zero at any positive price vector at which each agent has a demand (Proposition 2.5)'. Proposition 2.5 (line 110) is stated 'Assume A1, A3 and A4 ... let x^1 and x^2 be demands at q'. Matches. 'Two agents trade one good in each state' matches §1 (line 55).",
    },
    {
        "id": "E4a-r12-delta-L02-L568",
        "check": "2.9-prose (delta)",
        "location": "L02.html line 568 (quiz item 9 explanation)",
        "status": "PASS",
        "evidence": "'(§4)': §4 is 'An equilibrium in closed form' (line 166) and contains Proposition 2.9 (line 169), the logarithmic-utility construction. Correct reference. Item 9 answer ('It exhibits an equilibrium for the logarithmic economy, and it does not prove existence for other economies') matches Proposition 2.9 and A5.",
    },
    {
        "id": "E4a-r12-delta-L03-L361",
        "check": "2.2-numbers / 2.4-math (delta)",
        "location": "L03.html line 361 (E2 solution)",
        "status": "PASS",
        "evidence": "Re-verified (see E4a-r8-delta-L03-E2 in this round). The sentence 'The conclusion that the endowment is not Pareto efficient rests on the hand witness of Problem R2, not on the count' is consistent with R2 (line 386) and with the twin output 'pareto_improvements_on_grid_at_endowment 2'.",
    },
    {
        "id": "E4a-r12-delta-index-L63-L09",
        "check": "2.9-DAG (delta)",
        "location": "index.html line 63 (adverse selection clause); L09.html line 37 (Uses list)",
        "status": "PASS",
        "evidence": "'From E2 it uses adverse selection, which Lesson 9 lists among its uses.' L09.html line 37 'Uses:' list includes 'adverse selection (contrast only)' linked to concepts.html#adverse-selection. True as written. E2 L03 h1 'Adverse Selection' is the owner title.",
    },
    {
        "id": "E4a-r12-ruling13-L03-keyrow3",
        "check": "2.3-grades (ruling 13)",
        "location": "L03.html line 407 (key results row 3, MRS values)",
        "status": "PASS",
        "evidence": "Row 3 (T; 'Derived in Example 3.6 from Proposition 2.9; reproduced exactly by Lab 3 Part A') has the Example as its basis, as ruling 13 requires for values derived by hand in a numbered Example. Example 3.6 (line 118) computes the MRS values by hand from the formula of Definition 3.3 and the Example 2.11 bundles; the re-derivation gives 4, 2, 1/2 for both agents and the price ratios 4, 2, 1/2 (rederive_slice_a12.py PASS).",
    },
    {
        "id": "E4a-r12-ruling13-L03-keyrow5",
        "check": "2.3-grades (ruling 13)",
        "location": "L03.html line 409 (key results row 5)",
        "status": "PASS",
        "evidence": "C with basis 'Lab 3 Part B, a finite enumeration on a grid; not a proof', as ruling 13 requires for a lab-only count. The count is reproduced by rederive_slice_a12.py (125, 0, 2).",
    },
    {
        "id": "E4a-r12-banned-and-process-scan",
        "check": "2.9-prose",
        "location": "index.html, L01.html, L02.html, L03.html visible text; tests/labs/E4 twins",
        "status": "PASS",
        "evidence": f"{SCR}/banned_scan.py: 0 hits (banned phrases, process words, ellipses) on the four pages. Twins grep: no process word other than the ordinary 'rounding'.",
    },
    {
        "id": "E4a-r12-rederive-slice-a",
        "check": "2.2-numbers / 2.4-math (full slice)",
        "location": "index.html, L01.html, L02.html, L03.html, lab twins L01-L03",
        "status": "PASS",
        "evidence": f"{SCR}/rederive_slice_a12.py: 61 PASS, FAILS 0. Covers every number of Example 1.5, Props 1.7 and 1.10 values, Problems M1-M3, P1-P3, E1-E3, R1-R3 of L01; Remark 2.6, Example 2.11, M1-M3, P2, R1-R3, misconceptions 1-3, Lab 2 Part D and E of L02; Example 3.6, the grid counts, R2 derivatives, E2 witness of L03; Prop 2.8 maximization on 20000 random budget bundles ({OUTS}/rederive.out).",
    },
    {
        "id": "E4a-r12-gates-and-pytest",
        "check": "2.5-labs / tooling",
        "location": "tools check_pages, check_dag, check_projects, run_labs, build_site, render_curriculum --check, verify_refs --offline, page_smoke, ruff, mypy, pytest, run_graders",
        "status": "PASS",
        "evidence": f"Every command in {SCR}/run_commands.sh exit 0 (outputs in {OUTS}/exit_codes.txt); run_graders, verify_refs --offline and pytest run separately with exit 0. Pytest (tests/test_labs.py, test_run_labs.py, test_page_checks.py) dots only.",
    },
]

rows: list[dict[str, str]] = []
undecided: list[str] = []
for rid, prow in prev_rows.items():
    loc = prow.get("location", "")
    if rid in CARRY:
        files = CARRY[rid]
        rows.append({
            "id": rid,
            "check": prow["check"],
            "location": loc,
            "status": "PASS",
            "evidence": CARRY_NOTE.format(files=files, pin=PREV_PIN) + prow["evidence"],
        })
    elif rid in REVERIFY:
        status, ev = REVERIFY[rid]
        rows.append({"id": rid, "check": prow["check"], "location": loc, "status": status, "evidence": ev})
    elif rid in {r["id"] for r in FAIL_ROWS}:
        continue
    else:
        undecided.append(rid)
        continue

# Rows that FAIL this round keep their round-11 ids (E4a-r6-math-keyresults, E4a-r6-grades-claims, E4a-r8-delta-L01-references)
# and the two new ruling-13 rows. Round-11 FAIL rows are fixed and re-verified above.
fail_ids = {"E4a-r6-math-keyresults", "E4a-r6-grades-claims", "E4a-r8-delta-L01-references"}
for fr in FAIL_ROWS:
    if fr["id"] in fail_ids:
        prow = prev_rows[fr["id"]]
        rows.append({"id": fr["id"], "check": prow["check"], "location": prow["location"], "status": "FAIL",
                     "evidence": fr["evidence"], "fix": fr["fix"]})
    else:
        rows.append({"id": fr["id"], "check": fr["check"], "location": fr["location"], "status": "FAIL",
                     "evidence": fr["evidence"], "fix": fr["fix"]})
for nr in NEW_ROWS:
    rows.append(nr)

if undecided:
    raise SystemExit("round-11 rows without a round-12 decision: " + ", ".join(undecided))
# Every round-11 id must appear exactly once.
ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate row id"
missing = set(prev_rows) - set(ids)
assert not missing, f"round-11 ids dropped: {sorted(missing)}"

fails = [r for r in rows if r["status"] != "PASS"]
verdict = "PASS" if not fails else "FAIL"

fragment = {
    "unit": "E4",
    "slice": "a",
    "round": 12,
    "verifier": "Haiku independent verifier, E4-a round 12 (did not build E4; no shared context with the builders or the round-11 verifier)",
    "pin": PIN,
    "base": (
        f"{PREV_PIN} (round-11 pin). Slice-a delta git diff 11d7077 5db69a9: index.html line 63; L01.html lines 51, 104, 253-254, 280; "
        "L02.html lines 51, 568; L03.html line 361; tests/labs/E4/lab-E4-L01-1.py lines 93-94; plans/FINAL-ARCHITECT-RULINGS.md item 13 "
        "(T versus C for worked values, applied to slice a)."
    ),
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE12-E4-a (detached at 5db69a9, .venv symlinked)",
    "scratch": "/tmp (twin outputs /tmp/e4-v-a12-L01.out, L02.out, L03.out); all scripts and outputs under ledgers/E4/scripts/E4-a-r12/",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice a has no project grader: mutation testing, the ten student-error mutants and the five alternatives do not apply (plan ruling: lab twins are demonstrations; mutation applies to project graders only).",
        "Round-11 FAIL rows are fixed and re-verified PASS: E4a-r11-delta-L02-L568 (L02 line 568 now '(§4)') and E4a-r11-lab-L01-partE-label (twin and page now 'overweight').",
        "New FAIL under architect ruling 13 (plans/FINAL-ARCHITECT-RULINGS.md item 13, added in 5db69a9): the four-state values of Lab 1 (340/3, 56, 596/3, 235/4) are graded T with no numbered Example deriving them, and the L02 residuals of Lab 2 are graded T with a Proposition basis. Both must be C naming the lab, or be derived by hand in a numbered Example (see the two ruling-13 rows).",
        "Out of slice (cards.json, slice F, not verified here): cards E4-c011, E4-c012, E4-c013 and E4-c015 (Lab 1 values graded T with basis 'Lab 1, Part B/C/D'), and E4-c033, E4-c034, E4-c035 (Lab 2 residuals and ratios graded T with basis 'Lab 2'), conflict with ruling 13 and must be re-graded with the lesson rows.",
        "Round-12 gate outputs are archived under ledgers/E4/scripts/E4-a-r12/outputs/. Live verify_refs was not run (network); the offline registry run passed and the slice cites no key.",
        "Observations (not rows): L01 line 51 cross-references Definition 1.6 and Proposition 1.4 in the why-it-matters paragraph before their definitions, as the round-11 text did for Definitions 1.2 and 1.3; accepted as introductory cross-references.",
    ],
    "summary": (
        f"Slice a (index.html, L01-L03, lab twins L01-L03), round 12 at 5db69a9: {len(rows)} rows; "
        f"{sum(1 for r in rows if r['status'] == 'PASS')} PASS, {len(fails)} FAIL, 0 UNVERIFIABLE. "
        "FAIL under ruling 13 (lab-only values graded T): L01 key-results row 5 (line 427) and its references sentence (line 511); "
        "L02 key-results row 6 (line 487). Round-11 FAIL rows are fixed."
    ),
}

OUT.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("rows", len(rows), "fails", len(fails), "verdict", verdict)
