"""Round-13 BK4-c: write the fragment ledgers/BK4/BK4-c.json from the rows verified this round.

Mutants are parsed from the saved mutation-gate output (out/mutate_BK4_seeds0-9_r13.txt), so each killed_by is the test
the tool reported. Run from the checkout root: python3 -I ledgers/BK4/scripts/BK4-c-r13/write_fragment_r13.py
"""

import json
import os
import re
from datetime import UTC, datetime

ROOT = os.getcwd()
S = "ledgers/BK4/scripts/BK4-c-r13"
O = f"{S}/out"

rows = []


def row(id_, check, location, status, evidence, fix=None):
    item = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        item["fix"] = fix
    rows.append(item)


# ---- tools and gates -------------------------------------------------------------------------------------------------
row("proj-check-tools", "2.6 autograder (check tools)", "course/modules/BK/BK4/project.html",
    "PASS", f"check_projects --unit BK4: 'check_projects BK4: PASS' exit 0 ({O}/check_projects.txt); check_pages --unit "
    f"BK4: PASS exit 0 ({O}/check_pages.txt); check_dag --unit BK4: PASS exit 0 ({O}/check_dag.txt).")
row("proj-ruff", "2.6 autograder (ruff)", "tests/labs/BK4; course/modules/BK/BK4/grader", "PASS",
    f"ruff check: 'All checks passed!' ({O}/ruff_check.txt); ruff format --check: '12 files already formatted' "
    f"({O}/ruff_format.txt).")
row("proj-mypy-repo", "2.6 autograder (mypy)", "pyproject.toml [tool.mypy]", "PASS",
    f"mypy --no-incremental over the repository: 'Success: no issues found in 385 source files' ({O}/mypy_repo.txt).")
row("proj-mypy-plan-command", "2.6 autograder (mypy)", "course/modules/BK/BK4/grader/test_project.py:28, :30", "PASS",
    f"mypy --no-incremental tests/labs/BK4 course/modules/BK/BK4/grader: 'Success: no issues found in 12 source files' "
    f"({O}/mypy_unit.txt).")
row("proj-pytest-labs", "2.5 lab (pytest)", "tests/test_labs.py; tests/test_run_labs.py; tests/test_page_checks.py",
    "PASS", f"pytest -k 'BK4 or bk4 or BK' over tests/test_labs.py, test_memo_exemplars.py, test_page_checks.py, "
    f"test_run_labs.py: 8 passed (out: {O}/pytest_BK4_r13.txt).")
row("proj-page-smoke", "2.9 structure (page_smoke)", "course/modules/BK/BK4/project.html", "PASS",
    f"page_smoke --unit BK4 --pages project.html: 'page_smoke BK4: PASS' exit 0 ({O}/page_smoke_project_r13.txt). The "
    "tool loads the page in Chromium, pastes the reference solution into the in-browser grader and requires every test "
    "to pass (tools/page_smoke.py docstring lines 34-35), with zero console errors and zero external requests.")
row("proj-refs", "2.1 citations", "course/modules/BK/BK4/project.html reading list (data-cite duffie2011central, "
    "bisndcpmi); page line 503 attributes no statement", "PASS",
    f"verify_refs --unit BK4 (live): 'live re-verification of BK4: 3 of 560 entries, 0 problems' ({O}/"
    f"verify_refs_BK4_live_r13.txt); verify_refs --offline: '560 entries, 0 problems' ({O}/verify_refs_offline_all_r13.txt). "
    "references/references.json entries list used_by BK4 for duffie2011central, bisndcpmi and bisndbasel.")
row("proj-anchors-links", "2.9 structure", "course/modules/BK/BK4/project.html", "PASS",
    f"prose_scans_r13.py: 30 hrefs, 14 anchors, broken []. ({O}/prose_scans_r13.txt)")
row("proj-banned-and-process-words", "2.9 structure", "course/modules/BK/BK4/project.html; grader/*.py; "
    "tests/labs/BK4/lab-BK4-project-*.py", "PASS",
    f"check_pages BK4 PASS (banned strings, BUILDER_RULES 1.3-1.4); prose_scans_r13.py process-word regex over the page, "
    f"the four grader files and the three lab twins: no hits ({O}/prose_scans_r13.txt).")
row("proj-dag-concepts", "2.9 DAG", "course/modules/BK/BK4/project.html", "PASS",
    f"check_dag --unit BK4 PASS. The page has 0 concept links (data-concept count 0). By-name scan of all 1138 "
    f"curriculum concept names against the page: only central-counterparty and operational-risk match, both owned by BK4 "
    f"(in the closure). Closure from coursekit.prerequisite_closure('BK4') = E1, FC1, M1, M2, P0.1 ({O}/prose_scans_r13.txt).")
row("proj-notation-T", "2.4 notation", "course/modules/BK/BK4/project.html (Conventions 220-225; Inputs 200)", "PASS",
    f"The page has 0 math delimiters. No bare T and no registered symbol (notation/notation.json: T, Phi, gamma_3, gamma_4, "
    f"R^*, R^{{e*}}, R_f, Q) appears. Local letters L, S, K, M, R, D, t, k, Lambda, IM_d, DF_i, DF_d, a1-a3, N, i are each "
    f"defined on the page before use (Conventions 220-225; Inputs line 200). ({O}/prose_scans_r13.txt)")
row("proj-l03-crossref", "2.9 DAG; 2.4 math", "course/modules/BK/BK4/project.html:224, :223, :421, :417, :54; "
    "course/modules/BK/BK4/L03.html:51, :133, :143-146, :151, :415, :419", "PASS",
    "project.html:224 says Lesson 3 defines the cover and states the sizing rule with its proof under its own assumptions. "
    "L03.html:133 Definition 2.1 (margin cover level); :143-146 Assumptions A3 and A4; :151 Proposition 2.3 (the sized margin "
    "is an order statistic), T-graded with its proof in Part 2; :415 section 3 'Where the canon breaks' and :419 'No close-out "
    "period is modelled' (the close-out reference at project.html:417); :51 defines 'scenarios' (the scenario reference at "
    "project.html:54). L03 is read here only for these locators; its own slice is verified elsewhere.")
row("proj-grade-scale-citation", "2.3 grades", "course/modules/BK/BK4/project.html:421", "PASS",
    "project.html:421 quotes the scale as B 'published but not settled' and C 'working paper, practitioner research or single "
    "sample'. L01.html:45-46 reads 'published, not settled' (B) and 'working paper, practitioner research or single sample' (C).")
row("proj-reading-list-no-claim", "2.1 citations (attribution)", "course/modules/BK/BK4/project.html:503-506", "PASS",
    "project.html:503 says the page 'attributes no statement to either' registry source; the two data-cite items are "
    "list entries only, so no attributed claim is checked. The Duffie and Zhu abstract was not read (not needed: no claim).")
row("proj-atlas-studio", "2.6 atlas milestones; studios", "course/modules/BK/BK4 (no atlas key; plan section 8)", "PASS",
    "BK4 has no Atlas milestone and is not a studio: check_projects --unit BK4 PASS; plan section 8 and check_projects.py "
    "skip the contract check when no atlas key exists (tools/check_projects.py:144-146).")

# ---- labs ------------------------------------------------------------------------------------------------------------
row("proj-lab1-numbers", "2.5 lab; 2.2 numbers", "course/modules/BK/BK4/project.html:56-139; tests/labs/BK4/"
    "lab-BK4-project-1.py (changed in e919577: Fraction)", "PASS",
    f"run_labs --unit BK4 PASS 8/8 (code equals twin, twin passes python -I -W error, output equals expected block; "
    f"{O}/run_labs.txt). Independent recomputation ({S}/recompute_r13.py, out/recompute_r13.txt): layers 50000 / 6000 / "
    "20000, residual 4000, pool 12000, floored shares 1333/1666/1000 with leftover 1 to member 1 (1334), k = 39 from exact "
    "position 191/5, margin 117088, cover 9750 at the margin and 9500 one cent below. The page states 191/5, which the "
    "Fraction print reproduces.")
row("proj-lab2-numbers", "2.5 lab", "course/modules/BK/BK4/project.html:141-190; tests/labs/BK4/lab-BK4-project-2.py",
    "PASS", f"run_labs PASS (completion rule: every page line equals its twin line or contains ___; ({O}/run_labs.txt)). "
    "Completed blanks: shares = residual * FUND // pool and index = -((-target*count)//10000) give 1334/1666/1000, k 39, "
    f"margin 117088 (recompute_r13.py). Twin unchanged since round 12.")
row("proj-lab3-numbers", "2.5 lab; 2.2 numbers", "course/modules/BK/BK4/project.html:252-368; tests/labs/BK4/"
    "lab-BK4-project-3.py", "PASS",
    f"run_labs PASS. recompute_r13.py reproduces every printed line: Part A rows 20000 (margin), 55000 (50000 + 5000), 70000 "
    "(50000 + 6000 + 14000), 80000 (1334/1666/1000), 100000 (uncovered 12000) with conservation True; Part B targets 9000/9500/"
    "9750 give k 36/38/39, margins 105154/111074/117088, covers 9000/9500/9750, one cent below 8750/9250/9500, brute force "
    "agrees; Part C 9500: 2 past margin, 2 past fund, 0 past capital, 0 uncovered; 9000: 4, 2, 0, 0 (out/recompute_r13.txt).")
row("proj-labs-simulated-stdlib", "2.5 lab; 2.8 SIMULATED", "tests/labs/BK4/lab-BK4-project-1..3.py; project.html:54, "
    ":56-58, :141-146, :252-258", "PASS",
    "Each lab docstring says SIMULATED (twin 1 line 61, twin 2 line 147, twin 3 line 258) and the page says so (54, 56, 141, "
    "252). Imports are standard library only: lab 1 'import random' and 'from fractions import Fraction' (lines 7-8); lab 2 "
    "'import random' (line 6); lab 3 'import random' (line 8). No open() or network call in any twin.")
row("proj-lab2-learner-text", "2.12 process words; 2.5 lab", "course/modules/BK/BK4/project.html:143-146, :190; "
    "lab-BK4-project-2.py", "PASS",
    "Lab 2 hypothesis and interpretation read in full; the instructions name the expression each blank needs and no process "
    "word appears (prose_scans_r13.py).")
row("proj-lab3-claim-checks-rules", "2.5 lab; 2.2 numbers", "course/modules/BK/BK4/project.html:255, :367", "PASS",
    "Every claim in the Lab 3 hypothesis and interpretation was recomputed: five waterfall rows add to their losses; "
    "the 100000-cent row is the only row with an uncovered loss (12000); three sizing indices 36, 38 and 39; one cent below each "
    "margin falls short; Part C counts 2 and 4 past the margin and 0 past capital or survivors for the 9500 and 9000 margins "
    f"(recompute_r13.py, {O}/recompute_r13.txt).")

# ---- structure, prose and numbers --------------------------------------------------------------------------------------
row("proj-rung-ladder", "2.6 spec ladder", "course/modules/BK/BK4/project.html:41-50, :43, :193-216", "PASS",
    "Four rungs in order: worked example (Lab 1, line 45), completion problem (Lab 2 with two blanks, line 46, graded "
    "instantly), independent project (line 47), stretch (line 48, not graded). Tier U, so rungs 1 and 2 are full length "
    "(line 43). check_projects PASS.")
row("proj-hours", "2.9 hours", "course/modules/BK/BK4/project.html:34, :36, :374-387; course/modules/BK/BK4/index.html:29, :42, :161-174",
    "PASS", "data-hours-project 15 (line 34); eyebrow '15 hours' (line 36); table#hours sums 2+2+3+3+2+2+1 = 15 (lines 377-384). "
    "index.html:29 data-hours-project 15; index.html:42 '15 h project (30% of the 50 module hours)'. 15/50 = 30 %.")
row("proj-hours-estimates", "2.6 hours (verifier estimate)", "course/modules/BK/BK4/project.html:377-384", "PASS",
    "Verifier's own estimates: rung 1 1.5-2 h; rung 2 1.5-2 h; waterfall with six named refusals and the remainder rule 2-3 h; "
    "sizing and integer cover 1.5-2.5 h; edge cases and local suite 1.5-2 h; memo 1.5-2 h; self-assessment 0.5-1 h. Total "
    "about 10.5-14.5 h, inside 30 % of 15 h (10.5-19.5 h).")
row("proj-named-conditions", "2.9 structure (named conditions)", "course/modules/BK/BK4/project.html:204-212; "
    "grader/test_project.py:455-585, :880-975, :1023-1072", "PASS",
    "Six named conditions on page (204-212): margin_for_cover empty losses, target below 1 or above 10000, negative loss in "
    "margin_for_cover and cover_bps, cover_bps empty losses, waterfall negative amount, waterfall defaulter not a member. Each "
    "is tested on both sides of its limit (refusal and acceptance tests at 0/1 and 10000/10001, 0/-1 for amounts, 0 and 9/3/4 "
    "for ids). The message wording tests match the page: 'at least one scenario is needed', 'losses cannot be negative', and "
    "the names of the inputs.")
row("proj-conventions-prose", "2.4 math", "course/modules/BK/BK4/project.html:220-225; grader/reference.py:31-109", "PASS",
    "Layer order a1 = min(L, IM_d), a2 = min(L - a1, DF_d), a3 = min(L - a1 - a2, K), R = L - a1 - a2 - a3 "
    "(reference.py:57-60); survivors pro rata with leftover (reference.py:72-80); cover floored with <= (reference.py:108-109); "
    "sizing index -((-t*S)//10000) (reference.py:99). The reference passes the 87-test suite (proj-grader-reference-run).")
row("proj-fixture-tables", "2.4 math; 2.6 autograder", "course/modules/BK/BK4/project.html:228-251; grader/test_project.py:276-350, "
    "366-376, 638-675, 768-781", "PASS",
    "All 11 layer-order rows (losses 80 to 300), the 3 remainder rows (1, 2, 4 cents), the 4 sizing fixtures (8000 -> 40, 8001 -> "
    "50, 10000 -> 50, 5000 on four losses -> 20) and the 2 cover fixtures (3333, 6666) are tested. Recomputed independently "
    "(recompute_r13.py: sizing and cover fixtures; hand-checked layer rows; the 87-test suite passes on the reference).")
row("proj-money-integer-claim", "2.4 math", "course/modules/BK/BK4/project.html:204, :225; grader/test_project.py:186-194, :1023",
    "PASS", "The money fields are tested as plain int (checked_int, test_waterfall_returns_plain_int_money, test_cover_bps_is_an_int, "
    "test_the_margin_is_an_int_in_cents). Page line 225 says a survivor's share and a cover are exact fractions floored by integer "
    "division, which reference.py:73 and :108-109 do.")
row("proj-large-cent-claim", "2.6 mutation", "course/modules/BK/BK4/project.html:203-224; grader/test_project.py:438-447", "PASS",
    "Fixture funds 6692931089932558 and 585467024498971, loss 6585696953829388: floored shares 6055950114045319 and "
    "529746839784068, leftover 1 to member 1 gives 6055950114045320 (the test value). Residual times fund exceeds 2**53 "
    f"(recompute_r13.py, {O}/recompute_r13.txt).")
row("proj-sizing-duplicate-losses", "2.4 math", "course/modules/BK/BK4/project.html:224; grader/test_project.py:690-704, :816-822",
    "PASS", "Page: 'S scenario losses' (Conventions, count of the list). Tests count each occurrence: [5,5,10,20] at 5000 -> 5; "
    "[5,5,5,9,12] at 6000 -> 5; cover [5,5,10,20] at 5 -> 5000. Mutants r3a, r3b, r3e killed.")
row("proj-zero-loss-sizing", "2.6 mutation", "grader/test_project.py:707-714", "PASS",
    "[0,10,20,30] at 5000 -> 10 (k = 2 counts the zero). Mutant r5c killed by test_zero_losses_are_scenarios_in_the_sizing.")
row("proj-zero-loss-cover", "2.6 mutation", "grader/test_project.py:824-829", "PASS",
    "cover_bps([0,0,5,9], 0) = 5000 (two of four scenarios covered). Mutant r5d killed by test_zero_losses_are_in_the_cover_denominator.")
row("proj-remainder-spec", "2.4 math", "course/modules/BK/BK4/project.html:249; grader/test_project.py:361-388", "PASS",
    "Remainder fixture on page: loss 1 -> {1:1,2:0,3:0}, loss 2 -> {1:1,2:1,3:0}, loss 4 -> uncovered 1 with each survivor 1. "
    "Tests at 366-403 assert exactly these values.")
row("proj-survivor-leftover-order", "2.6 autograder mutation", "grader/test_project.py:406-425", "PASS",
    "Leftover goes to the lowest id with DF > 0 whatever the dictionary order (test_leftover_cent_goes_to_the_lowest_id..., "
    "test_a_member_with_no_default_fund_is_skipped...). Mutants r4a, r5a, s01, n3 killed.")
row("proj-silence-named-refusals", "2.6 autograder (silence)", "grader/test_project.py:1023-1072; mutants r4g, r4h",
    "PASS", "test_the_module_prints_nothing_on_valid_inputs and test_refused_inputs_print_nothing_before_they_raise (capsys). "
    "Mutants r4g (debug print on defaulter refusal) and r4h (debug print on uncovered loss) killed.")
row("proj-refusal-count-docstring", "2.6 autograder", "grader/test_project.py:1034-1035", "PASS",
    "The docstring says 'Each named refusal in the list below raises ValueError and prints nothing'; the list holds 16 entries "
    "covering the named conditions. No count is stated, so none is checked.")
row("proj-grader-docstring-named-variables", "2.6 autograder (failure messages)", "grader/test_project.py:1-15", "PASS",
    "Docstring: each expected result is held in a named variable and '--assert=plain' hides values. Asserts compare named "
    "variables (want, want_survivors, expected); the run uses --assert=plain (project.html:400; py-worker.js:111).")
row("proj-failure-leak", "2.6 autograder (failure messages)", "grader/test_project.py (all helpers and asserts)", "PASS",
    "Every failure message was read. None prints an expected value; the interpolated values are inputs (losses, targets, "
    "condition labels), e.g. 'seeded scenario with loss {loss}' (line 250) and 'margin_for_cover at target {target}' (line 620).")
row("proj-context-sentences", "2.9 structure", "course/modules/BK/BK4/project.html:198 (dd of dt 'Context')", "PASS",
    "The Context dd has four sentences (defaults, the simulator, the sizing, the autograder).")
row("proj-spec-context-length", "2.9 structure", "course/modules/BK/BK4/project.html:198", "PASS",
    "Four sentences in the Context dd, as above; check_projects PASS.")
row("proj-spec-signatures", "2.6 autograder (spec)", "course/modules/BK/BK4/project.html:202; grader/starter.py:29-47", "PASS",
    "Names and signatures on the page match starter.py: waterfall(loss_cents, defaulter_id, initial_margin_cents, "
    "default_fund_cents, ccp_capital_cents); margin_for_cover(losses_cents, target_bps); cover_bps(losses_cents, margin_cents); "
    "Waterfall fields margin_cents, default_fund_cents, ccp_capital_cents, survivor_cents, uncovered_cents.")
row("proj-spec-inputs-instance", "2.6 autograder (instances)", "course/modules/BK/BK4/project.html:200; grader/instance.py:22-50",
    "PASS", "Page: N from 4 to 6 with ids 1..N; default funds at least 1 cent; S from 40 to 80; targets 9000/9500/9750. "
    f"instance.py:25, :28, :33, :39 match; instance_check_r13.py confirms on seeds 0-49 ({O}/instance_check_r13.txt).")
row("proj-spec-questions", "2.6 spec (clarifying questions)", "course/modules/BK/BK4/project.html:196-216", "PASS",
    "Questions a competent student would ask and their answers on the page: the order of the layers (line 220), the pro rata and "
    "leftover rule (221), the uncovered loss (221), zero contributions (221), the member ids (202: keys of default_fund_cents), "
    "the refusals (204-212), whether to read instance.py (200, 398). None is open.")
row("proj-local-run", "2.6 autograder (local run)", "course/modules/BK/BK4/project.html:398-400; grader/test_project.py:1-7",
    "PASS", "The command on the page is the one in the test file's docstring. Run on the reference copy with QF_SEED=0: 87 passed.")
row("proj-autograder-claims", "2.9 structure", "course/modules/BK/BK4/project.html:392, :521", "PASS",
    "Browser run (grader.js:95 runPytest with QF_SEED); seed derived from the workspace (grader.js:33, :53, text 'derived from your "
    "workspace ID', matching project.html:200). The footer's 'nothing you write leaves it' is consistent with page_smoke's "
    "zero-external-request check.")
row("proj-pyodide-empty-packages", "2.6 autograder (Pyodide)", "course/modules/BK/BK4/project.html:393 (no data-packages); "
    "course/assets/js/grader.js:29; course/assets/js/py-worker.js:28, :118", "PASS",
    "Absent data-packages gives [] (grader.js:29 filter(Boolean)); prepare() skips loadPackage for an empty list (py-worker.js:28); "
    "pytest is always loaded (py-worker.js:118). page_smoke ran the grader in-browser (proj-page-smoke). Plan section 11 item 10 "
    "is settled for this page.")
row("proj-round7-prose-delta", "2.9 structure (delta since round-12 pin)", "course/modules/BK/BK4/project.html hunks at "
    ":44, :47, :55-58, :63-66, :109-117, :131-138, :202, :215, :417", "PASS",
    "Delta 5db69a9b..e919577b for project.html: 23 changed lines. Each hunk read and verified: rung 3 wording 'memo section' "
    "(:47, :202); Lab 1 hypothesis '191/5' (:58); Fraction import and print (:66, :113-117, :132-138); the 87-check count (:215); "
    "C5 close-out parenthetical (:417). Every changed statement is true on the lab output (proj-lab1-numbers).")
row("proj-exemplar-a-calibration", "2.6 rubric (calibration)", "course/modules/BK/BK4/project.html:426-455", "PASS",
    f"Blind scoring of memo prose with verdict, annotation and score attributes removed ({S}/exemplar_blind_r13.py, "
    f"{O}/exemplar_memo_prose_r13.txt): C1 2 (all four layers named, no cents), C2 2 (sizing rule for 9500, no cover check), C3 1 "
    "(no rule, no amounts), C4 2 (margin with no cover), C5 2 (two limits). Official data-scores 2,2,1,2,2 (line 426): match "
    "exactly. Disclosure: the full page had been read before this scoring.")
row("proj-exemplar-b-calibration", "2.6 rubric (calibration)", "course/modules/BK/BK4/project.html:457-483", "PASS",
    "Blind scoring from the same prose: C1 4, C2 4 (target, k 38, 38th loss, cover 9500 and 9250), C3 4 (pro rata, leftover, "
    "payments sum to 4000), C4 4 (one margin with cover, two past margin and zero uncovered, one alternative), C5 4 (four "
    "limits with direction, no B/C claim, no source). Official data-scores 4,4,4,4,4 (line 457): match exactly.")
row("proj-exemplar-b-numbers", "2.2 numbers", "course/modules/BK/BK4/project.html:459-471 (exemplar B memo)", "PASS",
    "Each number traced: margins 30000/50000/40000/20000, funds 4000/6000/5000/3000, capital 20000, 40 losses (Lab 1 code, "
    "lines 68-70 and 110); 80000 loss, 4000 residual, 12000 pool (computed); floored 1333/1666/1000 and 1334/1666/1000 "
    "(Lab 1 expected lines 132-133); k 38 and 38.0 (9500*40/10000, computed); 111074, 9250, 105154, 117088, 9000, 9750 (Lab 3 "
    "expected lines 361-363); 2 past margin and 4 past margin, 0 past capital and survivors (lines 365-366); 5920 and 500 bps are "
    "differences of printed values. No unprinted or underived number.")
row("proj-rubric-c1-levels", "2.6 rubric (observable)", "course/modules/BK/BK4/project.html:413", "PASS",
    "Each level is observable from the memo: layer names and order, cents for a stated scenario, the 'used only after' statement.")
row("proj-rubric-c2-levels", "2.6 rubric (observable)", "course/modules/BK/BK4/project.html:414", "PASS",
    "Observable: target in bps, value of k, sorted position, cover at the margin and one cent below.")
row("proj-rubric-c3-descriptors", "2.6 rubric (observable)", "course/modules/BK/BK4/project.html:415", "PASS",
    "Each clause is checkable: named rules (pro rata, leftover), survivor amounts, a sum that checks them. The level 2 "
    "descriptor is long, but each branch maps to a memo property; not vague.")
row("proj-rubric-c4-descriptors", "2.6 rubric (observable)", "course/modules/BK/BK4/project.html:416", "PASS",
    "Observable: one margin, its cover, the count of scenarios past the survivors or uncovered, one alternative; a fallback margin "
    "is counted as a second recommendation (explicit).")
row("proj-rubric-c5-descriptor", "2.6 rubric (observable)", "course/modules/BK/BK4/project.html:417", "PASS",
    "Four limits named, direction for each, counter-evidence or 'cites none'. The close-out parenthetical points to Lesson 3 "
    "Section 3, which contains 'No close-out period is modelled' (L03.html:419).")
row("proj-rubric-observable-wording", "2.6 rubric (observable)", "course/modules/BK/BK4/project.html:409-417", "PASS",
    "All 20 descriptors read. No descriptor relies on an unobservable judgement; the only soft wording is the 'counts as stating it' "
    "clause, which is explicit.")
row("proj-exemplar-annotations-agree", "2.6 rubric (annotations)", "course/modules/BK/BK4/project.html:444-453, :473-481",
    "PASS", "Exemplar A annotations (levels 2,2,1,2,2 with one miss at C2 level 3) and exemplar B annotations (all level 4) agree "
    "with the data-scores attributes.")
row("proj-rubric-self-form", "2.6 rubric (form)", "course/modules/BK/BK4/project.html:485-489; course/assets/js/rubric.js:4",
    "PASS", "section.rubric-self has data-rubric='rubric' (table id at line 409) and data-exemplars 'exemplar-a exemplar-b' (ids "
    "at 426 and 457); rubric.js reads the exemplar article and data-scores.")
row("proj-alternatives", "2.6 autograder (five alternatives, plus two verifier alternatives)",
    "ledgers/BK4/alternatives/alt1..alt7", "PASS",
    f"{S}/run_alts_r13.py ran all seven on seeds 0-49: alt1 50/50, alt2 50/50, alt3 (Fraction) 50/50, alt4 (integer, two pass) "
    f"50/50, alt5 (bisection) 50/50, alt6 (Decimal at 100 digits and heapq, new) 50/50, alt7 (divmod and ceiling-add, new) 50/50 "
    f"({O}/alts_seeds_0-49_r13.txt). None is a float implementation.")
row("proj-mutants-builder", "2.6 mutation", "ledgers/BK4/mutants/m01..m10", "PASS",
    f"tools/mutate_graders.py --unit BK4 --seeds 0-9 (output {O}/mutate_BK4_seeds0-9_r13.txt): m01..m10 KILLED.")
row("proj-mutants-own", "2.6 mutation", "ledgers/BK4/mutants/n1..n4, r3a..r5f", "PASS",
    "Same run: n1-n4, r3a-r3f, r4a-r4h, r5a-r5f KILLED on seed 0.")
row("proj-mutants-round7", "2.6 mutation", "ledgers/BK4/mutants/s01..s05", "PASS", "Same run: s01-s05 KILLED.")
row("proj-mutants-round8", "2.6 mutation", "ledgers/BK4/mutants/t8a..t8e", "PASS", "Same run: t8a-t8e KILLED.")
row("proj-mutants-round9", "2.6 mutation", "ledgers/BK4/mutants/v9a..v9e", "PASS", "Same run: v9a-v9e KILLED.")
row("proj-mutants-round10", "2.6 mutation", "ledgers/BK4/mutants/x10a..x10d", "PASS", "Same run: x10a-x10d KILLED.")
row("proj-mutants-round11", "2.6 mutation", "ledgers/BK4/mutants/y11a..y11d", "PASS", "Same run: y11a-y11d KILLED.")
row("proj-mutants-round12", "2.6 mutation", "ledgers/BK4/mutants/r12a, r12c, r12d", "PASS",
    "Same run: r12a KILLED by test_layers_and_survivor_payments_add_to_the_loss_on_every_scenario; r12c and r12d KILLED by the same test.")
row("proj-mutant-float-index", "2.6 mutation (round-12 FAIL, now re-verified)", "ledgers/BK4/mutants/r12b_sizing_index_float.py; "
    "grader/test_project.py:678-687", "PASS",
    "Round-12 FAIL cleared. The new test test_exact_position_is_an_integer_index_not_a_rounded_float (target 2800 bps, 50 losses, "
    "expected 14) KILLS r12b on seed 0 (mutate output). Float check: 2800/10000*50 = 14.000000000000002 (recompute_r13.py), so "
    "math.ceil gives 15, while the exact integer index is 14. The test states an exact answer any correct implementation gives "
    "(alt1-alt7 pass it).")
row("proj-mutant-float", "2.6 mutation", "ledgers/BK4/mutants/vc10_float_arithmetic.py", "PASS",
    "KILLED by test_large_cent_shares_are_floored_in_integers on seed 0 (mutate output).")
row("proj-mutant-argument", "2.6 mutation", "ledgers/BK4/mutants/r4f_sizing_sorts_caller_list_in_place.py", "PASS",
    "KILLED by test_margin_for_cover_and_cover_bps_do_not_change_their_list_argument on seed 0.")
row("proj-mutants-round13", "2.6 mutation (new mutants, verifier-written)", "ledgers/BK4/mutants/r13a..r13c", "PASS",
    "Four new single-change mutants written by the verifier from reference.py (scripts/BK4-c-r13/make_r13_mutants.py). "
    "r13a (leftover only to survivors whose share is positive) KILLED by test_fixture_loss_181_is_the_first_cent_for_the_survivors; "
    "r13b (uncovered = residual - pool in both branches, negative below the pool) KILLED by "
    "test_layers_and_survivor_payments_add_to_the_loss_on_every_scenario; r13c (cover loop skips the last scenario, divides by "
    "S) KILLED by test_loss_equal_to_the_margin_is_covered. Diffs: mutant_diff_r13.py shows each differs from reference by one "
    "statement (no equivalent candidates).")
row("proj-mutant-fund-capped-at-pool", "2.6 mutation (a stated behaviour survives)",
    "ledgers/BK4/mutants/r13d_fund_layer_capped_at_survivor_pool.py; grader/test_project.py (layer-order fixtures, :276-350); "
    "project.html:220 (layer order: 'the default fund pays a2 = min(L - a1, DF_d)')", "FAIL",
    "Mutant caps the defaulter's default fund at the survivors' pool. It SURVIVES the mutation gate (mutate_BK4_seeds0-9_r13.txt: "
    "'SURVIVED r13d ... -> None') and all 50 seeds (probes_r13.txt: 'killed on 0 of 50 seeds'). The page states the rule it "
    "breaks (project.html:220: a2 = min(L - a1, DF_d), with no pool cap). No fixture or seed has DF_d above the survivors' pool "
    "(all fixtures have pool 100 or more; instance funds are 1000-8000 with 3-5 survivors). A sibling probe that caps the capital "
    "or the margin at the pool is killed (proj-cap-layer-probes), so the gap is specific to the fund layer. fixture_probe_r13d.py "
    "shows the candidate fixture separates the two.",
    "Add a hand-computed fixture to grader/test_project.py in the layer-order section (no seed): defaulter 3 with initial margin "
    "100 and default fund 50, CCP capital 30, survivors 1 and 2 with default funds 10 and 20 and margins 0. Call "
    "waterfall(200, 3, {1: 0, 2: 0, 3: 100}, {1: 10, 2: 20, 3: 50}, 30) and expect layers (100, 50, 30), survivor_cents "
    "{1: 7, 2: 13} and uncovered 0. The reference gives exactly this (fixture_probe_r13d.py); the r13d mutant gives fund 30, "
    "survivors {1: 10, 2: 20} and uncovered 10, so the fixture kills it. The page needs no change: the rule is already stated "
    "at project.html:220.")
row("proj-cap-layer-probes", "2.6 mutation (sibling probes)", "scripts/BK4-c-r13/probes_r13.py (not counted mutants)", "PASS",
    "The capital capped at the survivors' pool is KILLED on 45 of 50 seeds and the margin capped at the pool on 49 of 50 "
    f"({O}/probes_r13.txt). Only the fund layer cap escapes, which localises the gap in proj-mutant-fund-capped-at-pool.")
row("proj-direction-claims", "2.2 directional claims (rule 7)", "course/modules/BK/BK4/project.html:471 (exemplar B Limits paragraph; the same claims are the page's limit rules)", "PASS",
    f"Numeric check ({S}/direction_check_r13.py, out/direction_check_r13.txt): adding loss to every scenario never lowers the "
    "sized margin and never raises the cover at a fixed margin (21000 trials, 0 violations); a margin that rises in stress "
    "lowers the real cover's gap to the simulated one in the stated direction (3000 trials, 0 violations). The page's 'biases "
    "the sized margin down and the cover up' and its stress sentences are true.")
row("proj-scope-words", "2.12 scope words", "course/modules/BK/BK4/project.html (prose, 50 hits)", "PASS",
    f"prose_scans_r13.py lists 50 scope-word hits ({O}/prose_scans_r13.txt). Each is a definition (every cover is an integer), a "
    "stated rule (a layer is used only after the one before), a verified claim ('the only row of Part A with an uncovered loss': "
    "recompute shows only 100000), a reference to the seed or the instance ('None is market data'), or a rubric descriptor. The "
    "'every one of them' (line 229) is confirmed by the suite run.")
row("proj-numbers-rounding", "2.2 numbers (rounding)", "course/modules/BK/BK4/project.html:58, :112-113, :139, :251, :384",
    "PASS", "38.2 printed as 191/5 (Fraction) and as 38.2 in prose (exact); '95.00 %' = 38/40 and '95.50 %' = 9550 bps; "
    "'6666.67 to two places' = 20000/3; '30 %' = 15/50; the tolerance 1e-6*(1+|x|) is below one cent for every number printed in "
    "Lab 2 (largest 117088: 0.117). No prose figure differs from its unrounded value.")
row("proj-page-prose-delta-ruling", "2.9 structure (architect rulings)", "plans/FINAL-ARCHITECT-RULINGS.md 4 (deploy rule); "
    "plans/BK4-build-plan.md architect ruling 2026-11-04 (1)-(3)", "PASS",
    "Ruling 3 satisfied: no period-convention sentence on the page (prose_scans_r13.py). Ruling 2 satisfied: empty losses on "
    "cover_bps is on the page (:209) and in the grader (test_empty_losses_are_refused_in_cover_bps...). Ruling 1 (exemplar A level 2, "
    "B level 4) satisfied (data-level 426, 457). Ruling 4 (no deploy step) is a recorded owner item, not a defect of this slice.")

# ---- autograder reference, starter, count, instances, placement ---------------------------------------------------
row("proj-grader-reference-run", "2.6 autograder (reference)", "course/modules/BK/BK4/grader/reference.py; grader/test_project.py",
    "PASS", f"run_graders --unit BK4 --seeds 0-49: 'run_graders BK4: PASS (reference 50/50 seeds, slowest 1.2 s)' exit 0 "
    f"({O}/run_graders_0-49.txt). Also the reference copied as clearing_house.py with QF_SEED=0 under the browser flags: 87 passed.")
row("proj-grader-starter-fails", "2.6 autograder (starter)", "course/modules/BK/BK4/grader/starter.py", "PASS",
    f"The starter on seed 0: 83 failed, 4 passed; the 4 passes are test_waterfall_is_a_frozen_dataclass_with_the_named_fields "
    "(the starter defines the dataclass) and three instance-only tests (seeded case validity, regions, sizing spread). The 83 "
    f"failures carry the named message 'has no implementation for' ({O}/probes_r13.txt). The suite as a whole fails on the starter.")
row("proj-collect-count", "2.6 autograder (test count)", "course/modules/BK/BK4/project.html:215; grader/test_project.py",
    "PASS", "pytest --collect-only -q on the reference copy: '87 tests collected'; the page says the suite 'runs 87 checks' "
    "(project.html:215). The grep count of 'def test_' is 87 as well.")
row("proj-instances", "2.6 autograder (instances, 20 sampled)", "course/modules/BK/BK4/grader/instance.py:22-50", "PASS",
    f"instance_check_r13.py checks all of seeds 0-49, which includes the 20 a verifier must sample: validity (ids 1..N with N 4-6, "
    "aligned lists, DF >= 1, IM >= 0, K >= 0, defaulter a member, S 40-80, target in the set), determinism, and one loss in each "
    f"region (within margin, within fund, past every layer). 50 distinct sized margins; 3 targets; defaulter ids 1-5 ({O}/"
    "instance_check_r13.txt). Seed 0 margin 73529 matches the m10 mutant's message.")
row("proj-placement-claim", "2.9 structure", "course/modules/BK/BK4/project.html:43; course/modules/BK/BK4/index.html:69, :119, :124",
    "PASS", "project.html:43 says a placement diagnostic on the module page needs the mastery bar and both skill checks. index.html:69 "
    "has #placement with data-mastery 0.8; index.html:119 and :124 are two data-skill items. The claim holds.")

# ---- mutant list ----------------------------------------------------------------------------------------------------
mutants = []
for line in open(f"{O}/mutate_BK4_seeds0-9_r13.txt", encoding="utf-8"):
    m = re.match(r"^(KILLED|SURVIVED) (\S+): (.*) -> (\S+)(?: \(seed \d+\))?$", line.strip())
    if not m:
        continue
    status, name, description, killer = m.groups()
    mutants.append({"id": name, "description": description,
                    "killed_by": None if killer == "None" else killer})
assert len(mutants) == 79, len(mutants)

fragment = {
    "unit": "BK4",
    "slice": "BK4-c",
    "round": 13,
    "verifier": "Claude Haiku 5.5, independent verifier E13 for BK4-c (round 13); did not build BK4",
    "pin": "e919577b45b431ce68e1e6533b00b8a301277937 (HEAD of claude/fanout-b3; detached checkout)",
    "base": "5db69a9b (round-12 pin, the previous fragment's pin); delta 5db69a9b..e919577b for the slice: project.html (23 changed "
            "lines), grader/test_project.py (+12: test_exact_position_is_an_integer_index_not_a_rounded_float), "
            "tests/labs/BK4/lab-BK4-project-1.py (Fraction), ledgers/BK4/mutants r12a-r12d (added); read in full",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE13-BK4-c",
    "scratch": "/tmp/bk4c_r13",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Read in full: project.html (523 lines, all of it including the exemplars and the self-assessment block); "
        "grader/instance.py (50), reference.py (109), starter.py (47), test_project.py (1128, every test and helper); the three "
        "project twins and their page blocks; the seven alternatives (alt1-alt5 read in full; alt6, alt7 written and read by the "
        "verifier); all 79 mutants (each diffed against reference.py by ledgers/BK4/scripts/BK4-c-r13/mutant_diff_r13.py; bodies "
        "not each read line by line, their docstrings and single changes were checked by the tool).",
        "Blind scoring disclosure: the full page had been read before the exemplars were scored, so the blind is partial. The "
        "scorer then used only the memo prose extracted by exemplar_blind_r13.py (verdict, annotation and score attributes "
        "removed); both exemplars matched the official scores exactly.",
        "Reference deployment (FINAL-ARCHITECT-RULINGS 4): reference.py ships in the repository; not a defect of this slice.",
        "Not checked: a visual render of the page (it has no figures); a Pyodide run for every seed (page_smoke runs one seed in "
        "the browser; the suite runs on seeds 0-49 under local CPython); the Duffie and Zhu abstract (no claim is attributed); "
        "L01-L05 and the hub and cards (other slices); timing of the suite in Pyodide (under 60 s and 5 s per test, not measured).",
        "Round-12 FAIL proj-mutant-float-index is cleared (new test kills r12b). The new round-13 FAIL is "
        "proj-mutant-fund-capped-at-pool (a stated layer-order rule survives); its fix is a fixture, not a page change.",
        "Gate runs: check_projects, check_pages, check_dag, run_labs, run_graders --seeds 0-49, ruff, mypy (unit and repo) all "
        f"PASS; mutate_graders --seeds 0-9 FAIL 78/79 (the only survivor is r13d). See {O}/.",
    ],
    "summary": {},
}
counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
fragment["summary"] = {
    "rows": len(rows), "pass": counts["PASS"], "fail": counts["FAIL"], "unverifiable": counts["UNVERIFIABLE"],
    "mutants_killed": sum(1 for m in mutants if m["killed_by"]), "mutants_total": len(mutants),
    "text": f"BK4-c round 13: {counts['PASS']} PASS, {counts['FAIL']} FAIL, {counts['UNVERIFIABLE']} UNVERIFIABLE of "
            f"{len(rows)} rows; mutants {sum(1 for m in mutants if m['killed_by'])}/{len(mutants)} killed. FAIL: "
            "proj-mutant-fund-capped-at-pool (a survivor that violates the stated a2 = min(L - a1, DF_d) rule). Exemplars "
            "calibrate exactly; alternatives 7/7 pass seeds 0-49; reference 50/50; 87 tests collected = page.",
}
# Normalise every bare name of a script or output of this round to its repository path (VERIFIER_RULES section 3).
SCRIPTS = {"recompute_r13.py", "instance_check_r13.py", "direction_check_r13.py", "mutant_diff_r13.py",
           "fixture_probe_r13d.py", "prose_scans_r13.py", "exemplar_blind_r13.py", "run_alts_r13.py",
           "make_r13_mutants.py", "probes_r13.py", "write_fragment_r13.py", "run_gates.sh"}
OUTPUTS = {"mutate_BK4_seeds0-9_r13.txt", "probes_r13.txt", "recompute_r13.txt", "instance_check_r13.txt",
           "direction_check_r13.txt", "prose_scans_r13.txt", "exemplar_memo_prose_r13.txt",
           "alts_seeds_0-49_r13.txt", "pytest_BK4_r13.txt", "page_smoke_project_r13.txt",
           "verify_refs_BK4_live_r13.txt", "verify_refs_offline_all_r13.txt", "run_labs.txt",
           "run_graders_0-49.txt", "check_projects.txt", "check_pages.txt", "check_dag.txt", "ruff_check.txt",
           "ruff_format.txt", "mypy_unit.txt", "mypy_repo.txt"}
NAME = re.compile(r"(?<![/\w.-])(?:out/)?([A-Za-z0-9_.-]+\.(?:py|txt|sh))(?![\w.-])")


def repository_path(text):
    def swap(match):
        name = match.group(1)
        if name in SCRIPTS:
            return f"{S}/{name}"
        if name in OUTPUTS:
            return f"{O}/{name}"
        return match.group(0)
    return NAME.sub(swap, text)


def normalise(value):
    if isinstance(value, str):
        return repository_path(value)
    if isinstance(value, list):
        return [normalise(v) for v in value]
    if isinstance(value, dict):
        return {k: normalise(v) for k, v in value.items()}
    return value


fragment = normalise(fragment)
with open(os.path.join(ROOT, "ledgers/BK4/BK4-c.json"), "w", encoding="utf-8") as handle:
    json.dump(fragment, handle, ensure_ascii=False, indent=2)
    handle.write("\n")
print("wrote ledgers/BK4/BK4-c.json:", fragment["summary"]["text"])
