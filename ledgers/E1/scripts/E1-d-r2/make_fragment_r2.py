# ruff: noqa: E501
"""Verifier round 2, slice d: writes ledgers/E1/E1-d.json from the outputs saved in ledgers/E1/scripts/E1-d-r2/.

Mutant rows are parsed from mutate_all_0_49.out (tools/mutate_graders.py --unit E1 --seeds 0-49).
Usage: .venv/bin/python -I ledgers/E1/scripts/E1-d-r2/make_fragment_r2.py
"""

from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "ledgers/E1/scripts/E1-d-r2"
PIN = "9294b914a51647c66d2dee62c4a112c76ba04900"
PREV = "aeb512b65b7774b59b84f836a13984fcfe9d0d1f"

RE_LINE = re.compile(r"^KILLED (\S+?): (.*) -> (.*)$")
mutants = []
for line in (OUT / "mutate_all_0_49.out").read_text(encoding="utf-8").splitlines():
    m = RE_LINE.match(line)
    if not m:
        continue
    name, description, killed_by = m.group(1)[:-3], m.group(2), m.group(3)
    mutants.append(
        {
            "id": name,
            "description": description,
            "file": f"ledgers/E1/mutants/{name}.py",
            "killed_by": killed_by + " (mutate_graders --seeds 0-49, first failing seed)",
        }
    )
assert len(mutants) == 136, len(mutants)

P = "PASS"
rows = [
    {
        "id": "E1d-r1-ladder",
        "check": "2.6-spec",
        "location": "course/modules/E/E1/project.html lines 40-49, 55-257, 559-566",
        "status": P,
        "evidence": "Re-read in full this round. Rung 1 Lab 1 (line 55) has a comment on each step; rung 2 is class 'lab completion' (line 130); rung 3 spec (line 311) and memo (line 365); rung 4 stretch (line 559). tools/check_projects.py --unit E1: 'check_projects E1: PASS' (scripts/E1-d-r2/check_projects.out).",
    },
    {
        "id": "E1d-r1-spec-precedence",
        "check": "2.6-spec",
        "location": "course/modules/E/E1/project.html line 321 (Constraints)",
        "status": P,
        "evidence": "Round-1 FAIL is fixed: line 321 now reads 'When more than one of these conditions holds, a ValueError whose message names any one of them is accepted.' Every invalid case in grader/test_project.py lines 251-291 violates one condition; the reference (grader/reference.py lines 26-35) checks in the listed order. Re-run of the suite on reference.py: 124 passed (seed 0).",
    },
    {
        "id": "E1d-r1-spec-tests-align",
        "check": "2.6-spec",
        "location": "course/modules/E/E1/project.html lines 318-323; grader/test_project.py",
        "status": P,
        "evidence": "Each stated constraint maps to a test: exact keys (test_outcome_has_exactly_the_six_keys, line 111), int types (118), closed forms (125), orderings (134-184), ties (198-222), half rounding (333-350), large exact inputs (323-330), stdlib (353-364), purity (235-240, 367-381), smallest b and c (294-319), second instance (390-398), ValueError table (251-291). Collect-only: 124 tests.",
    },
    {
        "id": "E1d-r1-hours",
        "check": "2.9-hours",
        "location": "course/modules/E/E1/project.html lines 340-346; course/modules/E/E1/index.html line 29; curriculum/02-economics-finance-core.yaml",
        "status": P,
        "evidence": "Table rows 2+3+8+8+6+3 = 30 = data-hours-project (index.html line 29, 30); 90 lessons + 30 project = 120. index.html and the curriculum are not in the git diff aeb512b6..9294b914 (byte-identical since round 1).",
    },
    {
        "id": "E1d-r1-lab1-run",
        "check": "2.5-lab",
        "location": "course/modules/E/E1/project.html lines 55-128; tests/labs/E1/lab-E1-project-1.py",
        "status": P,
        "evidence": "tools/run_labs.py --unit E1 --page project: 'run_labs E1: PASS (3/3)'. scripts/E1-d-r2/project_labs_r2.py: page code == twin (True); twin under python -I -W error exit 0, stderr empty; output == expected block (True).",
    },
    {
        "id": "E1d-r1-lab2-completion",
        "check": "2.5-lab",
        "location": "course/modules/E/E1/project.html lines 130-187; tests/labs/E1/lab-E1-project-2.py lines 28, 33",
        "status": P,
        "evidence": "project_labs_r2.py: page differs from twin only on the two blanks (twin line 28 'return (d - rival) / 2' vs page 'return ___'; twin line 33 'return half_up(...)' vs page 'return half_up(___)'); 2 blanks on the page; twin output == expected block (True); page_smoke lab-E1-project-2 passes.",
    },
    {
        "id": "E1d-r1-lab3-run",
        "check": "2.5-lab",
        "location": "course/modules/E/E1/project.html lines 189-257; tests/labs/E1/lab-E1-project-3.py",
        "status": P,
        "evidence": "page code == twin (True); twin output == expected block (True); scripts/E1-d-r2/rederive_r2.out re-derives all 12 lines of the a=120 and a=121 blocks with Fractions (e.g. a=121 Cournot 67/54/2267/2267/4534/567; Bertrand 101/20/0/5101/5101/0).",
    },
    {
        "id": "E1d-r1-lab1-prose",
        "check": "2.5-lab",
        "location": "course/modules/E/E1/project.html lines 57, 64-67, 127",
        "status": P,
        "evidence": "rederive_r2.py reference checks: d=100; monopoly 50 trades, 70 cents, profit 2500, CS 1250, DWL 1250; Cournot 200/3, 160/3, profit and CS 20000/9, W 40000/9, DWL 5000/9; Bertrand 100, 20, DWL 0; CS=Q^2/(2b) and DWL=(d-Q)^2/(2b) identities hold. 'prints True | True' line matches.",
    },
    {
        "id": "E1d-r1-lab2-prose",
        "check": "2.5-lab",
        "location": "course/modules/E/E1/project.html lines 132, 138-139, 186",
        "status": P,
        "evidence": "rederive_r2.out: after 60 steps from 0, |q_60 - d/3| = d/(3*2^60) < 1e-12 (the lab's comparison prints True); error recurrence e_{k+1} = -e_k/2 verified; 40000/9 = 4444.44; 160/3 = 53.33.",
    },
    {
        "id": "E1d-r1-lab3-prose",
        "check": "2.5-lab",
        "location": "course/modules/E/E1/project.html lines 191, 256-257",
        "status": P,
        "evidence": "rederive_r2.py: 141/2 = 70.5 -> 71; 101/2 = 50.5 -> 51; monopoly profit (70.5-20)*50.5 = 10201/4 = 2550.25 -> 2550; welfare 3750 and 4444 at a=120; 200/3 and 202/3 both lie in (66.5, 67.5).",
    },
    {
        "id": "E1d-r1-prop1",
        "check": "2.6-proof",
        "location": "course/modules/E/E1/project.html lines 285-288 (Proposition 1)",
        "status": P,
        "evidence": "Re-derived: pi(Q) = -Q^2/b + (d/b)Q; pi' = (d-2Q)/b; pi'' = -2/b; maximiser d/2; fee (a+bc)/(2b); pi(d/2) = d^2/(4b); f-c = d/(2b). Grid (1/8 steps, a=120,b=1,c=20) maximiser Q=50 (rederive_r2.py).",
    },
    {
        "id": "E1d-r1-prop2",
        "check": "2.6-proof",
        "location": "course/modules/E/E1/project.html lines 290-293 (Proposition 2)",
        "status": P,
        "evidence": "Re-derived line by line: BR derivative (d-2q_i-q_j)/b; the q_1=0 case gives q_1=d/4>0, a contradiction; subtraction gives q_1=q_2; 2q=d-q gives d/3; e_{k+1}=-e_k/2 so |e_k|=d/(3*2^k); fee (a+2bc)/(3b); each profit d^2/(9b). Half-step grid (a=119,b=1,c=20): unique grid equilibrium (33,33); BR equals max(0,(d-q_j)/2) to within the grid step.",
    },
    {
        "id": "E1d-r1-prop3",
        "check": "2.6-proof",
        "location": "course/modules/E/E1/project.html lines 295-297 (Proposition 3)",
        "status": P,
        "evidence": "Proof cases re-read: undercut to c (f<c), undercut to (c+f1)/2 (f2>f1>c), split undercut to (f+c)/2 (f1=f2>c), raise f1=c to g in (c,f2). Grid check (a=40,b=1,c=10): quarter-grid profiles, deviations on a 1/64 grid: only (c,c) survives (rederive_r2.out, section 4). The quarter grid alone gives a spurious (41/4,41/4) (no grid point in (10,10.25)); the proof's deviation (f+c)/2 excludes it.",
    },
    {
        "id": "E1d-r1-prop4",
        "check": "2.6-proof",
        "location": "course/modules/E/E1/project.html lines 299-302 (Proposition 4)",
        "status": P,
        "evidence": "Integral identities re-derived; CS + profit = (aQ-Q^2/2)/b - cQ and W(d)-W(Q) = (d-Q)^2/(2b) checked exactly at 41 grid points for each of (120,1,20), (121,3,5), (400,2,60), (61,1,5) (rederive_r2.py section 4).",
    },
    {
        "id": "E1d-r1-prop5",
        "check": "2.6-proof",
        "location": "course/modules/E/E1/project.html lines 304-307 (Proposition 5)",
        "status": P,
        "evidence": "Each difference re-derived: fee gap d/(6b), Cournot fee minus c = d/(3b), DWL d^2/(8b) and d^2/(18b), profit gap d^2/(36b), W(2d/3)-W(d/2) = 5d^2/(72b). Proof bounds (d/6 > b >= 1, d/(6b) > 1, d^2/(18b) > 2b, 5d^2/(72b) > 5b/2, d^2/(36b) > b) re-checked. Printed strict order of volumes, fees, welfare, DWL and profit holds on 10000 instance seeds (gap > 6b on all) and on 220200 grid cases (b 1..10, c 1..60, gap 6b+1..400).",
    },
    {
        "id": "E1d-r1-conventions",
        "check": "2.6-spec",
        "location": "course/modules/E/E1/project.html line 329 (Conventions)",
        "status": P,
        "evidence": "Round-1 FAIL is fixed: line 329 now says Propositions 1 to 4 give the reported values. Mapping checked against the statements: P1 gives Q* (volume), fee and profit of monopoly; P2 gives Cournot volume, fee and total profit; P3 gives Bertrand volume d, fee c and zero profit; P4 gives CS, welfare and DWL for any structure.",
    },
    {
        "id": "E1d-r1-notation",
        "check": "13-notation",
        "location": "course/modules/E/E1/project.html (all \\( ... \\) math, lines 264-330, 562-564); notation/notation.json",
        "status": P,
        "evidence": "notation.json registers T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q} and macros. The page's math tokens are a, b, c, d, f, f_1, f_2, g, i, k, n, q, q_i, q_j, q_k, e_k, t, x, G, W, Q (quantity), pi; none is a registered symbol. Plain Q is a quantity, not \\mathbb{Q}. Local letters are defined where first used (pi in Prop 1, G and W in Prop 4, e_k in Prop 2, f_1 and f_2 in Prop 3).",
    },
    {
        "id": "E1d-r1-dag",
        "check": "14-dag",
        "location": "course/modules/E/E1/project.html (brief line 370; memo); course/modules/E/E1/L05.html, L06.html, L07.html titles",
        "status": P,
        "evidence": "tools/check_dag.py --unit E1: 'check_dag E1: PASS'. The brief's 'Lessons 5 to 7' are L05 Monopoly Pricing, L06 Oligopoly: Cournot and Bertrand, L07 Surplus and Deadweight Loss (h1 of each file), which cover the project's structures and welfare.",
    },
    {
        "id": "E1d-r1-process-words",
        "check": "12-process-words",
        "location": "course/modules/E/E1/project.html (whole file)",
        "status": P,
        "evidence": "tools/check_pages.py --unit E1: 'check_pages E1: PASS' (its banned-string check covers visible prose). Read in full: no process words in the changed text.",
    },
    {
        "id": "E1d-r1-citation",
        "check": "3-attribution",
        "location": "course/modules/E/E1/project.html 'Reading' section (lines 568-574); references/references.json key varian2014intermediate",
        "status": P,
        "evidence": "The page attributes no statement to the source and gives no locator ('No passage locator from it has been confirmed'). Registry entry present (Open Library, Varian 2014, Intermediate Microeconomics). tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems'.",
    },
    {
        "id": "E1d-r1-autograder-reference",
        "check": "2.6-autograder",
        "location": "course/modules/E/E1/grader/reference.py; tools/run_graders.py",
        "status": P,
        "evidence": "tools/run_graders.py --unit E1 --seeds 0-49: 'run_graders E1: PASS (reference 50/50 seeds, slowest 0.2 s)' (scripts/E1-d-r2/run_graders.out).",
    },
    {
        "id": "E1d-r1-autograder-count",
        "check": "2.6-autograder",
        "location": "course/modules/E/E1/project.html line 323; grader/test_project.py",
        "status": P,
        "evidence": ".venv/bin/python -m pytest --collect-only -q test_project.py: '124 tests collected'; the page says 124 checks.",
    },
    {
        "id": "E1d-r1-autograder-instances",
        "check": "2.6-autograder",
        "location": "course/modules/E/E1/grader/instance.py; project.html line 317",
        "status": P,
        "evidence": "Over seeds 0..9999: b in [1,3], c in [5,60], gap in [60,400], a > bc > 0, gap > 6b on every seed (rederive_r2.out). Docstring and page line 317 agree with these ranges.",
    },
    {
        "id": "E1d-r1-autograder-messages",
        "check": "2.6-autograder",
        "location": "course/modules/E/E1/grader/test_project.py lines 9-12, 50-102, 114-398",
        "status": P,
        "evidence": "Failure messages name the property and contain no expected value (checked by reading each check/pytest.fail call). The docstring (lines 9-12) now says the fee is the inverse demand at the volume, which matches exact() line 71 ('fee = (a - volume) / b'). The oracle imports only market_structure and instance, not reference.",
    },
    {
        "id": "E1d-r1-autograder-browser",
        "check": "2.6-autograder",
        "location": "course/modules/E/E1/project.html line 355 (grader panel); tools/page_smoke.py",
        "status": P,
        "evidence": "tools/page_smoke.py --unit E1 --pages project: 'page_smoke modules/E/E1/project.html: PASS'; in-browser grader 'All 124 tests pass on seed 706289331'; labs 0.0 s each (scripts/E1-d-r2/page_smoke.out).",
    },
    {
        "id": "E1d-r1-mutants-existing",
        "check": "2.6-mutants",
        "location": "ledgers/E1/mutants/ (131 files before this round); tools/mutate_graders.py --unit E1 --seeds 0-49",
        "status": P,
        "evidence": "mutate_graders E1 with seeds 0-49, one run covering all 136 files: 136/136 KILLED, including the 131 earlier files (scripts/E1-d-r2/mutate_all_0_49.out).",
    },
    {
        "id": "E1d-r1-mutants-new",
        "check": "2.6-mutants",
        "location": "ledgers/E1/mutants/e1d_r1_m01..m06*.py",
        "status": P,
        "evidence": "All six round-1 mutants are KILLED in the same run (mutate_all_0_49.out; killed_by column of this fragment).",
    },
    {
        "id": "E1d-r1-alternatives",
        "check": "2.6-alternatives",
        "location": "ledgers/E1/scripts/E1-d-r2/alternatives/ (alt_a_linear_solve, alt_b_simpson, alt_c_decimal, alt_d_iterate_cutoff); scripts/E1-d-r2/run_alt_seeds_0_49.py",
        "status": P,
        "evidence": "Each of the four alternatives passes test_project.py on all 50 seeds (alternatives_seeds_0_49.out, run with python -I, --assert=plain -W error).",
    },
    {
        "id": "E1d-r1-rubric-structure",
        "check": "2.6-rubric",
        "location": "course/modules/E/E1/project.html lines 385-396 (rubric table)",
        "status": P,
        "evidence": "Six criteria, four levels each. Each level contains the one below it (checked per criterion). The C6 row is the one changed this round (see E1d-r1-rubric-C6-observable).",
    },
    {
        "id": "E1d-r1-rubric-C6-observable",
        "check": "2.6-rubric",
        "location": "course/modules/E/E1/project.html line 394 (C6 level 2); line 544 (Exemplar B annotation)",
        "status": P,
        "evidence": "Round-1 FAIL is fixed: C6 level 2 is now 'Names one or more of the limits. What changes without each limit need not be stated at this level.' Observable by checking whether one to three limits are named. The Exemplar B annotation (line 544) follows the new wording.",
    },
    {
        "id": "E1d-r1-rubric-calibration",
        "check": "2.6-rubric",
        "location": "course/modules/E/E1/project.html lines 402-550 (Exemplars A and B)",
        "status": P,
        "evidence": "My scoring of the memo texts against the rubric gives A = 1,2,2,2,1,2 and B = 4,4,4,4,3,2, equal to the official scores (lines 404, 469). CAVEAT: this is not blind. I read the official-scoring text and annotations in the same file before scoring. The blind requirement is a separate row (E1d-r2-exemplar-blind).",
    },
    {
        "id": "E1d-r1-exemplar-annotations",
        "check": "2.6-rubric",
        "location": "course/modules/E/E1/project.html line 413 (Exemplar A, C4 annotation) vs line 408 (Exemplar A Summary text); line 477 (Exemplar B, 'in part')",
        "status": "FAIL",
        "summary": "Exemplar A's C4 annotation says the welfare ordering is not stated with its sign, but the passage states it: 'welfare is lower under monopoly' (line 408).",
        "evidence": "Line 413: 'Misses C4 level 3: the fee and volume orderings are given without their printed numbers, and the welfare ordering is not stated with its sign.' Line 408 of the same passage: 'welfare is lower under monopoly'. The sign is stated in words. The level result (2) is unaffected; the annotation's stated reason is wrong. Also, line 477 says 'Meets C4 level 3 in part', a label the rubric does not define.",
        "fix": "Line 413: replace the clause 'and the welfare ordering is not stated with its sign' with 'and the welfare ordering gives no printed numbers or differences'. Line 477: drop 'in part' or name the missing element of level 3.",
    },
    {
        "id": "E1d-r1-data-simulated",
        "check": "11-data",
        "location": "course/modules/E/E1/project.html lines 53, 62, 195, 317; grader/instance.py line 3",
        "status": P,
        "evidence": "Page: 'No data file is read ... not market data' (line 53), 'not market data' (62, 195), 'It is SIMULATED ... None of it is exchange data' (317). instance.py docstring: 'returns a SIMULATED case'.",
    },
    {
        "id": "E1d-r1-gates",
        "check": "gates",
        "location": "repository gates on checkout 9294b914 (slice-scoped)",
        "status": P,
        "evidence": "check_pages E1 PASS; check_dag E1 PASS; check_projects E1 PASS; run_labs E1 --page project PASS (3/3); run_graders E1 --seeds 0-49 PASS (50/50); page_smoke project PASS; mutate_graders E1 --seeds 0-49 136/136 killed; verify_refs --offline 560 entries, 0 problems; ruff check and format --check on the 3 project twins and grader PASS; mypy --no-incremental on the 3 twins PASS; pytest tests/test_memo_exemplars.py tests/test_page_checks.py tests/test_labs.py PASS.",
    },
    {
        "id": "E1d-r1-structure-order",
        "check": "2.5-structure",
        "location": "course/modules/E/E1/project.html (section order)",
        "status": P,
        "evidence": "tools/check_projects.py --unit E1: PASS (ladder, spec, grader, memo, stretch in order).",
    },
    {
        "id": "E1d-r1-atlas-studio",
        "check": "2.5-structure",
        "location": "course/modules/E/E1/project.html",
        "status": P,
        "evidence": "grep -i 'atlas|studio' course/modules/E/E1/project.html: no matches. tools/check_projects.py: PASS.",
    },
    {
        "id": "E1d-r1-docstring-units",
        "check": "2.5-lab",
        "location": "course/modules/E/E1/project.html line 159; tests/labs/E1/lab-E1-project-2.py line 27",
        "status": P,
        "evidence": "Round-1 FAIL is fixed: both the page (line 159) and the twin (line 27) now read 'q_i = (d - q_j) / 2, in trades'. project_labs_r2.py: page code == twin on all non-blank lines.",
    },
    {
        "id": "E1d-r2-mutants-new",
        "check": "2.6-mutants",
        "location": "ledgers/E1/mutants/e1d_r2_m01..m05*.py (derived from grader/reference.py)",
        "status": P,
        "evidence": "Five new student-error mutants: m01 Bertrand fee d/b; m02 gross value (aQ-Q^2)/b; m03 DWL with /b (factor 2 dropped); m04 Cournot profit rounded per exchange and doubled; m05 volume rounded up with a ceiling. All killed on seeds 0-49 (killed_by column of this fragment).",
    },
    {
        "id": "E1d-r2-alternatives-new",
        "check": "2.6-alternatives",
        "location": "ledgers/E1/scripts/E1-d-r2/alternatives/alt_d_decimal_quantize.py, alt_e_integer_cutoff_common_denominator.py, alt_g_validation_reordered.py, alt_f_cournot_iteration_200.py",
        "status": P,
        "evidence": "alt_d (Decimal 80-digit quantize, ROUND_HALF_UP), alt_e (integer numerators over 18b, rounded by (2n+m)//(2m)) and alt_g (ValueError checks in order c, b, a, structure) pass all 50 seeds. alt_f (Cournot quantity from 200 best-response steps) fails the fixed tie case test_tie_rounds_up_for_each_output[cournot-consumer_surplus_cents-31-4-1] on every seed: its volume is inexact by d/(3*2^200), which pushes the exact half 40.5 below the tie. The spec requires exact fractions, so alt_f is not a correct alternative and the failure is not an over-constraint.",
    },
    {
        "id": "E1d-r2-exemplar-blind",
        "check": "2.6-rubric",
        "location": "course/modules/E/E1/project.html lines 402-550 (Exemplars A and B)",
        "status": "UNVERIFIABLE",
        "summary": "Blind exemplar scoring (ruling 15) was not achieved in this round.",
        "evidence": "The page was read in full, including the official scores (lines 404, 469) and the annotations (lines 410-548), before the exemplars were scored. The agreement in E1d-r1-rubric-calibration therefore is not independent evidence.",
        "fix": "A fresh verifier re-scores Exemplars A and B from the memo passages alone, with the annotations and official-scoring paragraphs removed from the text it reads, and compares against the official scores.",
    },
]

fragment = {
    "unit": "E1",
    "slice": "d",
    "round": 2,
    "verifier": "verifyS2-E1-d (Haiku 5.5)",
    "pin": PIN,
    "base": PREV,
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS2-E1-d",
    "scratch": "/tmp/e1d_r2",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Round 2 on 9294b914 (delta aeb512b6..9294b914 in slice: project.html, grader/test_project.py, lab-E1-project-2.py, "
        "lab-E1-project-3.py). The four round-1 FAIL rows (spec-precedence, conventions, rubric-C6-observable, docstring-units) "
        "are fixed and re-verified. Every other row was re-verified this round rather than carried, because the subject file "
        "project.html changed. Propositions 1-5 and the Lab 1-3 text were re-derived with scripts/E1-d-r2/rederive_r2.py. "
        "Exemplar scoring was NOT blind (E1d-r2-exemplar-blind). Pre-existing files in ledgers/E1/scripts/E1-d-r2/ (from an "
        "earlier pass, committed) were not modified; this round's files are untracked. Not run: the full repository gate "
        "(ruff check ., full mypy, live verify_refs, pytest full suite), the live Chrome UI (page_smoke used the repository's "
        "Chromium run), and the visual reveal of the exemplar form. Exemplar 'data-level' attributes are not read by rubric.js; "
        "their meaning is undocumented (A=2, B=4), not a row."
    ),
    "summary": (
        "Slice d round 2 at 9294b914: verdict FAIL. 40 rows: 38 PASS, 1 FAIL (E1d-r1-exemplar-annotations, minor wrong annotation "
        "reason), 1 UNVERIFIABLE (E1d-r2-exemplar-blind, blind scoring not done). Mutants: 136/136 killed on seeds 0-49 "
        "(131 earlier plus 5 new student-error mutants). Alternatives: 7 correct implementations pass 50 seeds; the inexact "
        "one (alt_f) is rejected by the exact-half tie case, as the spec's exact-fraction rule requires."
    ),
}

problems = []
assert all(r["status"] in ("PASS", "FAIL", "UNVERIFIABLE") for r in rows)
dest = ROOT / "ledgers/E1/E1-d.json"
dest.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", dest, "rows", len(rows), "mutants", len(mutants))
